import os
import sys
import time
import json
import PIL.Image
from tqdm import tqdm
from dotenv import load_dotenv
import google.generativeai as genai


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


from constants import *
from prompts.prompts_for_closed_models import *


def get_gemini_model():
    load_dotenv(dotenv_path=env_dir_path)

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    generation_config = {
        "temperature": 0,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    return model


def send_request(model, prompt_parts):
    retry_count = 0

    while retry_count < MAX_RETRY:
        try:
            response = model.generate_content(prompt_parts)
            return response.text
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(RETRY_DELAY)
            retry_count += 1

    return None


def get_closed_model_prompt(country, prompt_type, question):
    if prompt_type == "d":
        return get_direct_prompt(question)
    elif prompt_type == "cot_z":
        return get_cot_prompt_zero_shot(question)
    elif prompt_type == "cot_f":
        return get_cot_prompt_few_shot(question)
    elif prompt_type == "cot_f2":
        return get_cot_prompt_few_shot2(question)
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
    if prompt_type == "cot_f2":
        print("Current prompt - cot_few_shot_with_image")
        img1 = PIL.Image.open(cot_f2_example_image_path)

    no_response_file_reader = open(no_response_file, "w")

    with open(response_file, "w") as file:
        for ind, obj in enumerate(tqdm(data, desc="Processing items")):

            cnt += 1

            question = obj["question"]
            img = PIL.Image.open(obj["map_path"])
            prompt_parts = []
            if img1:
                prompt_parts.append(img1)

            prompt = get_closed_model_prompt(country, prompt_type, question)
            prompt_parts.append(prompt)
            prompt_parts.append(img)

            response = send_request(model, prompt_parts)

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
