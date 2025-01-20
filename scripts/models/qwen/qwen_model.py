import os
import sys
import time
import json
import torch
from tqdm import tqdm
from PIL import Image
from dotenv import load_dotenv
from modelscope import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from constants import *
from prompts.prompts_for_open_models import *

model_dir = snapshot_download("qwen/Qwen-VL", cache_dir=CACHE_DIR)
tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
tokenizer.pad_token = "<|endoftext|>"
tokenizer.padding_side = "left"


def get_qwen_model():
    torch_type = torch.bfloat16
    model = (
        AutoModelForCausalLM.from_pretrained(
            model_dir,
            cache_dir=CACHE_DIR,
            torch_dtype=torch_type,
            trust_remote_code=True,
        )
        .eval()
        .cuda()
    )

    return model


def askQwen(model, prompt_w_question, image_path):
    query = tokenizer.from_list_format(
        [
            {"image": image_path},
            {"text": prompt_w_question},
        ]
    )
    batch = [query]
    inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
    inputs.to(model.device)
    with torch.no_grad():
        outputs = None
        try:
            outputs = model.generate(**inputs)
        except Exception as e:
            print(e)
            print(inputs)
            print(batch)
    generated = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print(generated)
    return generated[0]


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

            response = askQwen(model, prompt, img_path)

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
