import os
import re
import sys
import json
import argparse
import importlib
import models.gemini.gemini_model as gemini
import models.cog.cog_model as cog
import models.internlm.internlm_model as internlm
import models.qwen.qwen_model as qwen


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from constants import *


def load_json_data(file_path: str) -> list:
    """
    For loading json data from the file
    structure of file: each line contains a json object
    """

    json_object_pattern = re.compile(r"({.*?})(?=\s*{|\s*$)", re.DOTALL)

    # Read the file content
    with open(file_path, "r") as file:
        file_content = file.read()

    # Find all JSON objects in the file content
    json_objects = json_object_pattern.findall(file_content)
    json_array = []
    # Process each JSON object
    for json_string in json_objects:
        try:
            # Parse the JSON object
            json_object = json.loads(json_string)
            # Do something with the json_object (for example, print it)
            json_array.append(json_object)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            print("JSON string was:", json_string)

    return json_array


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process some states and values.")

    parser.add_argument(
        "--model",
        type=str,
        required=True,
        choices=["gemini", "gpt4", "cog", "idefics", "internlm", "qwen"],
        help="Model Name",
    )

    parser.add_argument(
        "--country",
        type=str,
        required=True,
        choices=["usa", "india", "china", "orgs", "img", "shuff", "img"],
        help="The country to check",
    )

    parser.add_argument(
        "--map_type",
        type=str,
        required=True,
        choices=["w", "wo", "h"],
        help="Map Type",
    )

    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        choices=["d", "cot_z", "cot_f", "cot_f2", "eer"],
        help="Model Name",
    )

    parser.add_argument(
        "--random",
        action="store_true",
        help="Set this flag in order to shuffle the data",
    )

    parser.add_argument(
        "--sample_size",
        type=int,
        required=False,
        default=-1,
        help="An optional numeric value for specifing the number of responses",
    )

    args = parser.parse_args()

    model_name = args.model
    country_name = args.country
    map_type = args.map_type
    prompt_type = args.prompt
    random_flag = True if args.random else False
    sample_size = args.sample_size

    if map_type == "wo":
        map_type = "wo_annotations"
    elif map_type == "w":
        map_type = "with_annotations"
    elif map_type == "h":
        map_type = "hatched"
    else:
        print("Wrong Map Type !")
        raise Exception("Wrong Map Type")

    os.makedirs(responses_dir_path, exist_ok=True)
    os.makedirs(no_responses_dir_path, exist_ok=True)

    response_file_dir = f"{responses_dir_path}/{country_name}/{map_type}/"
    no_response_file_dir = f"{no_responses_dir_path}/{country_name}/{map_type}/"

    os.makedirs(response_file_dir, exist_ok=True)
    os.makedirs(no_response_file_dir, exist_ok=True)

    response_filename = (
        response_file_dir + f"{country_name}_{map_type}_{prompt_type}_response.json"
    )
    no_response_filename = (
        no_response_file_dir + f"{country_name}_{map_type}_{prompt_type}_response.json"
    )

    dataset_dir = None
    if country_name == "usa" or country_name == "india" or country_name == "china":
        dataset_dir = actual_map_paths
    else:
        dataset_dir = counter_factual_map_paths

    with open(
        f"{dataset_dir}/{country_name}/json_data/{country_name}_{map_type}_maps_data.json",
        "r",
    ) as file:
        json_data = json.load(file)

    if sample_size != -1:
        json_data = json_data[:sample_size]

    if model_name == "gemini":
        model = gemini.get_gemini_model()
        gemini.execute_store_response(
            json_data,
            model,
            country_name,
            prompt_type,
            response_filename,
            no_response_filename,
        )
    elif model_name == "cog":
        model = cog.get_cog_model()
        cog.execute_store_response(
            json_data,
            model,
            country_name,
            prompt_type,
            response_filename,
            no_response_filename,
        )

    elif model_name == "internlm":
        model = internlm.get_internlm_model()
        internlm.execute_store_response(
            json_data,
            model,
            country_name,
            prompt_type,
            response_filename,
            no_response_filename,
        )

    json_array = load_json_data(response_filename)
    # print(json_array)

    with open(response_filename, "w") as file:
        json.dump(json_array, file, indent=4)

    print("done")
