import os
import sys
import time
import json
import torch
from tqdm import tqdm
from PIL import Image
from transformers.image_utils import load_image
from transformers import AutoProcessor, AutoModelForVision2Seq


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from constants import *
from prompts.prompts_for_idefics import *


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_idefics_model():
    processor = AutoProcessor.from_pretrained("HuggingFaceM4/idefics2-8b")
    model = (
        AutoModelForVision2Seq.from_pretrained(
            "HuggingFaceM4/idefics2-8b",
            torch_dtype=torch.float16,
            _attn_implementation="flash_attention_2",
            cache_dir=CACHE_DIR,
            trust_remote_code=True,
        )
        .eval()
        .cuda()
        .half()
    )
    return model, processor


def askIdeFics(model, processor, message, image_path):

    img = load_image(image_path)
    prompt = processor.apply_chat_template(message, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[img], return_tensors="pt")
    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    # Generate
    generated_ids = model.generate(**inputs, max_length=4096, top_p=1, do_sample=False)
    generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)
    return generated_texts[0] if generated_texts else None


def get_idefics_model_prompt(country, prompt_type, question):
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
    data, model, processor, country, prompt_type, response_file, no_response_file
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

            prompt = get_idefics_model_prompt(country, prompt_type, question)

            response = askIdeFics(model, processor, prompt, img_path)

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
