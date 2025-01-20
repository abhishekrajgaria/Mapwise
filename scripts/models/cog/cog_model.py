import os
import sys
import time
import json
import torch
from tqdm import tqdm
from PIL import Image
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, LlamaTokenizer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from constants import *
from prompts.prompts_for_open_models import *

torch.set_grad_enabled(False)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = LlamaTokenizer.from_pretrained("lmsys/vicuna-7b-v1.5")
torch_type = torch.bfloat16


def get_cog_model():
    torch.set_grad_enabled(False)
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch_type = torch.bfloat16

    model = AutoModelForCausalLM.from_pretrained(
        "THUDM/cogagent-vqa-hf",
        cache_dir=CACHE_DIR,
        torch_dtype=torch_type,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
    )
    model = model.to(DEVICE)
    model.eval()
    return model


def ask_cog_agent(
    model, query, image_path, history=[], temperature=0.9, do_sample=False
):
    """
    Get the response from the cogagent based on the given image, query, and conversation history.

    Parameters:
    - image_path (str): Path to the image file.
    - query (str): The current query prompt.
    - history (list): List of tuples containing the conversation history.
    - temperature (float): Sampling temperature for response generation (default is 0.9).
    - do_sample (bool): Whether to use sampling during response generation (default is False).

    Returns:
    - str: The generated response from the cogagent.
    """

    tokenizer = LlamaTokenizer.from_pretrained("lmsys/vicuna-7b-v1.5")

    image = Image.open(image_path).convert("RGB")

    input_by_model = model.build_conversation_input_ids(
        tokenizer, query=query, history=history, images=[image]
    )
    inputs = {
        "input_ids": input_by_model["input_ids"].unsqueeze(0).to(DEVICE),
        "token_type_ids": input_by_model["token_type_ids"].unsqueeze(0).to(DEVICE),
        "attention_mask": input_by_model["attention_mask"].unsqueeze(0).to(DEVICE),
        "images": [[input_by_model["images"][0].to(DEVICE).to(torch_type)]],
    }
    if "cross_images" in input_by_model and input_by_model["cross_images"]:
        inputs["cross_images"] = [
            [input_by_model["cross_images"][0].to(DEVICE).to(torch_type)]
        ]

    gen_kwargs = {
        "max_length": 1024,
        "temperature": temperature,
        "do_sample": do_sample,
    }

    with torch.no_grad():
        outputs = model.generate(**inputs, **gen_kwargs)
        outputs = outputs[:, inputs["input_ids"].shape[1] :]
        response = tokenizer.decode(outputs[0])
        response = response.split("</s>")[0]
    return response


def get_open_model_prompt(country, prompt_type, question):
    if prompt_type == "d":
        return get_direct_prompt(question)
    elif prompt_type == "cot_z":
        return get_cot_prompt_zero_shot(question)
    elif prompt_type == "eer":
        return get_eer_prompt(question)
    elif prompt_type == "cot_z" and country == "img":
        return get_img_cot_zero_shot_with_dict(question, IMAGINARY_DICT)
    elif prompt_type == "eer" and country == "img":
        return get_img_eer_with_dict(question, IMAGINARY_DICT)
    elif prompt_type == "cot_z" and country == "shuff":
        return get_shuff_cot_zero_wo_dict(question)
    elif prompt_type == "eer" and country == "shuff":
        return get_shuff_eer_wo_dict(question)
    elif prompt_type == "cot_z_wd" and country == "shuff":
        return get_shuff_cot_zero_with_dict(question)
    elif prompt_type == "eer_wd" and country == "shuff":
        return get_shuff_eer_with_dict(question)
    else:
        print("Wrong Prompt Type !")
        raise Exception("Wrong Prompt Type")


def execute_store_response(
    data, model, country, prompt_type, response_file, no_response_file
):
    cnt = 0
    print("*****************************")
    print("Total Queries to be executed - ", len(data))
    img1 = None

    no_response_file_reader = open(no_response_file, "w")

    with open(response_file, "w") as file:
        for ind, obj in enumerate(tqdm(data, desc="Processing items")):

            cnt += 1

            question = obj["question"]
            img_path = obj["map_path"]

            prompt = get_open_model_prompt(country, prompt_type, question)

            response = ask_cog_agent(model, prompt, img_path)

            if response:
                obj["response"] = response
                json.dump(obj, file)
                file.write("\n")
            else:
                json.dump(obj, no_response_file_reader)
                no_response_file_reader.write("\n")

            delay = REQUEST_DELAY_FREE

            time.sleep(delay)

    no_response_file_reader.close()

    print("*****************************")
    print("Total Questions executed - ", cnt)
    print("*****************************")
