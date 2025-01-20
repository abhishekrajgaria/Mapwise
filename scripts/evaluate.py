import os
import re
import sys
import json
import time
import string
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from scipy.stats import kendalltau, spearmanr

import models.gemini.gemini_model as gemini

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from constants import *
from prompts.prompts_for_closed_models import get_non_dec_order

r_yn = "_"
c_or_d = "_"
abbrev_dict = {}
state_set = set()


def replace_abbrev(response: str) -> str:
    """
    Replaces abbreviations with full state name
    """

    for key in abbrev_dict.keys():
        response = response.replace(key, abbrev_dict[key])

    return response


def normalize_range(range: str) -> str:
    """
    Normalize the given range in the decimal format.
    """

    higher_data = None
    lower_data = None
    range = range.replace(" ", "")
    range = range.replace(",", "")

    def normalize_val(val: float, unit: str) -> float:
        if unit == "K" or unit == "k":
            val *= 1000
        elif unit == "M" or unit == "m":
            val *= 1000000
        elif unit == "B" or unit == "b":
            val *= 1000000000
        elif unit == "T" or unit == "t":
            val *= 1000000000000

        return val

    lower = ""
    higher = ""
    # check for both lower and higher number
    has_dash_in_middle = re.match(HAS_DASH_REGEX, range)
    if has_dash_in_middle:
        lower = has_dash_in_middle.group(1)
        higher = has_dash_in_middle.group(4)
    else:
        higher = range

    # Gets '<', '>' or '-' sign infront of the number, number and its unit like '%'
    higher_match = re.match(ARROW_VALUE_UNIT_REGEX, higher)
    higher_arrow_sign = higher_match.group(1) if higher_match.group(1) else ""
    higher_val = float(higher_match.group(2))
    higher_unit = higher_match.group(4) if higher_match.group(4) else ""

    if higher_unit == "" or higher_unit == "%":
        higher = f"{higher_arrow_sign}{higher_val}{higher_unit}"
    else:  # for K, M, B, T
        higher_val = normalize_val(higher_val, higher_unit)
        higher = f"{higher_arrow_sign}{higher_val}"

    range = f"{higher}"
    higher_data = [higher_arrow_sign, higher_val]

    if lower != "":
        lower_match = re.match(ARROW_VALUE_UNIT_REGEX, lower)
        lower_arrow_sign = lower_match.group(1) if lower_match.group(1) else ""
        lower_val = float(lower_match.group(2))
        lower_unit = lower_match.group(4) if lower_match.group(4) else higher_unit

        if lower_unit == "" or lower_unit == "%":
            lower = f"{lower_arrow_sign}{lower_val}{lower_unit}"
        else:
            lower_val = normalize_val(lower_val, lower_unit)
            lower = f"{lower_arrow_sign}{lower_val}"

        lower_data = [lower_arrow_sign, lower_val]

        range = f"{lower}-{higher}"

    return range, higher_data, lower_data


def isRange(str_to_check: str) -> bool:
    """
    Check if the given string is of type Range
    """
    has_dash_in_middle = False
    if isinstance(str_to_check, str):
        temp_answer = str_to_check.replace(" ", "")
        temp_answer = temp_answer.replace(",", "")
        has_dash_in_middle = re.search(HAS_DASH_REGEX, temp_answer)
    return (
        has_dash_in_middle
        or "<" in str_to_check
        or ">" in str_to_check
        or "%" in str_to_check
        or "N/A" in str_to_check
    )


def has_digit(text: str) -> bool:
    """
    Check if string has digit
    """
    return any(char.isdigit() for char in text)


def evaluate_range(ground_truth: str, response: str, c_or_d: str) -> float:
    """
    Equates the ground truth and response values.
    """

    response = response.replace("to", "-")
    response = response.replace("and", "-")
    response = response.replace("above", ">")
    response = response.replace("below", "<")

    # If the given response is not of type range or does not has digit than return False.
    if not (isRange(response) or has_digit(response)):
        return False

    ground_truth, ground_higher_data, ground_lower_data = (
        normalize_range(ground_truth) if "N/A" not in ground_truth else ("N/A", [], [])
    )

    response, response_higher_data, response_lower_data = (
        normalize_range(response) if "N/A" not in response else ("N/A", [], [])
    )

    # Direct check will handle exact same scenario and N/A
    if ground_truth == response:
        return 1.0

    # Both are non empty
    elif ground_truth != "N/A" and response != "N/A":

        if ground_higher_data and ground_lower_data:
            if response_higher_data and response_lower_data:
                # exact value match for both lower and upper bound of range
                if (
                    ground_lower_data[1] == response_lower_data[1]
                    and ground_higher_data[1] == response_higher_data[1]
                ):
                    return 1.0

                # if the map is countinous then look for overlap, if overlap
                # give partial marks default 0.5

                elif (
                    c_or_d == "c"
                    and response_lower_data[1] < ground_higher_data[1]
                    and response_higher_data[1] > ground_lower_data[1]
                ):
                    return 0.5

            # response contains single value, given partial marks
            else:
                if (
                    ground_lower_data[1] == response_higher_data[1]
                    or ground_higher_data[1] == response_higher_data[1]
                ):
                    return 0.5
        # ground truth only contains single value
        else:
            ground_val = ground_higher_data[1]

            # Here we only want to check if the ground value match to either response
            # higher or lower bound
            # It is very rare that ground truth range has a single value, but if yes
            # majority of time it is reflecting extreme values which is not accounted in the map
            # therefore giving full marks

            if response_higher_data[1] == ground_val or (
                response_lower_data and response_lower_data[1] == ground_val
            ):
                return 1.0

    # Neither equal nor overlapping in case of continuous map
    return 0.0


def compute_precision_recall(ground_truth: list, prediction: list) -> tuple:

    # Convert lists to sets to handle potential duplicates and to allow set operations
    ground_truth_set = set(ground_truth)
    prediction_set = set(prediction)

    # Compute True Positives (TP), False Positives (FP), and False Negatives (FN)
    true_positives = ground_truth_set.intersection(prediction_set)
    false_positives = prediction_set - ground_truth_set
    false_negatives = ground_truth_set - prediction_set

    # Precision: TP / (TP + FP)
    if len(prediction_set) > 0:
        precision = len(true_positives) / (len(true_positives) + len(false_positives))
    else:
        precision = 0.0

    # Recall: TP / (TP + FN)
    if len(ground_truth_set) > 0:
        recall = len(true_positives) / (len(true_positives) + len(false_negatives))
    else:
        recall = 0.0

    return precision, recall


def capitalize_first_letter(text: str, stop_words=["and"]):
    """
    Mainly required for matching the states name using the State dict
    in which each word in state names are capitalized
    example - New York, Rhode Island and others
    """

    # Split the text into words
    words = text.split()

    # Capitalize the first letter of each word if it's not a stop word
    capitalized_words = [
        word.capitalize() if word.lower() not in stop_words else word for word in words
    ]

    # Join the capitalized words back into a single string
    capitalized_text = " ".join(capitalized_words)

    return capitalized_text


def evaluate_list(ground_truth: str, response: str, country: str) -> tuple:
    """
    Evaluates Precision and Recall for the
    Ground Truth and Response
    """

    ground_truth = " ".join(ground_truth.split())
    response = " ".join(response.split())

    if country == "india":
        ground_truth = ground_truth.lower().replace(
            "jammu and kashmir", "jammu & kashmir"
        )
        response = response.lower().replace("jammu and kashmir", "jammu & kashmir")

    ground_truth = ground_truth.replace(" and ", " , ")
    ground_truth = ground_truth.replace(" or ", " , ")

    response = response.replace(" and ", " , ")
    response = response.replace(" or ", " , ")

    pattern = f"[{re.escape(string.punctuation)}]"

    ground_list = []
    for state in ground_truth.split(","):
        state = re.sub(pattern, "", state).strip()

        state = capitalize_first_letter(state)
        ground_list.append(state)

    response_list = []
    for state in response.split(","):
        state = re.sub(pattern, "", state).strip()

        state = capitalize_first_letter(state)
        response_list.append(state)

    ground_list = [state for state in ground_list if state in state_set]
    response_list = [state for state in response_list if state in state_set]
    precision, recall = compute_precision_recall(ground_list, response_list)

    ## Useful when both ground_list and response_list is None
    if ground_list == response_list:
        precision, recall = 1.0, 1.0

    return precision, recall


def parse_ranking_string(ranking_string: str) -> dict:
    """
    Convert the ranking string to dictionary
    like
    rank1: [stat1, stat2], rank2: [state3]
    """
    items = []
    current_item = ""
    relations = []
    for char in ranking_string:
        if char in ["<", ">", "="]:
            items.append(current_item.strip())
            items.append(char)
            current_item = ""
            relations.append(char)
        else:
            current_item += char
    items.append(current_item.strip())
    rank_dict = defaultdict(list)
    current_rank = 1
    min_rank = 1
    for i, item in enumerate(items):
        if item in ["<", ">", "="]:
            continue
        rank_dict[current_rank].append(item)
        if i < len(items) - 1:
            if items[i + 1] == "<":
                current_rank += 1
            elif items[i + 1] == ">":
                current_rank -= 1
                min_rank = min(min_rank, current_rank)
    if min_rank < 1:
        diff = 1 - min_rank
        rank_dict = {key + diff: value for key, value in rank_dict.items()}
    return rank_dict


def calculate_kendall_tau(ground_list: list, predicted_list: list) -> float:
    ground_ranks = {item: rank for rank, item in enumerate(ground_list)}
    predicted_ranks = [ground_ranks[item] for item in predicted_list]

    # Generate ranks
    ground_ranks_list = list(range(len(ground_list)))

    if len(predicted_ranks) != len(ground_ranks_list):
        ground_ranks_list = [
            rank for rank in ground_ranks_list if rank in predicted_ranks
        ]
        tau, _ = kendalltau(ground_ranks_list, predicted_ranks)
        if tau == 1.0:
            return 0
        else:
            return -1

    tau, _ = kendalltau(ground_ranks_list, predicted_ranks)
    return tau


def calculate_spearmanr_rho(ground_list: list, predicted_list: list) -> float:
    ground_ranks = {item: rank for rank, item in enumerate(ground_list)}
    predicted_ranks = [ground_ranks[item] for item in predicted_list]

    # Generate ranks
    ground_ranks_list = list(range(len(ground_list)))

    if len(predicted_ranks) != len(ground_ranks_list):
        ground_ranks_list = [
            rank for rank in ground_ranks_list if rank in predicted_ranks
        ]
        rho, _ = spearmanr(ground_ranks_list, predicted_ranks)

        if rho == 1.0:
            return 0
        else:
            return -1

    rho, _ = spearmanr(ground_ranks_list, predicted_ranks)
    return rho


def filter_items(ground_truth: list, predicted: dict) -> list:
    """
    This is used within ranking -
    we only want state names which are present in the ground truth
    """

    filtered_predicted = {
        rank: [item for item in items if item in ground_truth]
        for rank, items in predicted.items()
    }
    filtered_predicted = {
        rank: items for rank, items in filtered_predicted.items() if items
    }
    return filtered_predicted


def flatten_ranks(rank_dict: dict) -> list:
    return [item for rank in sorted(rank_dict) for item in rank_dict[rank]]


def compute_precision_at_k(ground_truth_order, predicted_order_list, k):
    """
    Compute Precision@k for a single query.

    Args:
    ground_truth_order (list): Ground truth ranking for a single query.
    predicted_order_list (list): Predicted ranking for a single query.
    k (int): Number of items to consider for precision computation.

    Returns:
    precision (float): Precision@k score.
    """
    num_correct = 0
    for item in predicted_order_list[:k]:
        if item in ground_truth_order:
            num_correct += 1
    precision = num_correct / k if k > 0 else 0
    return precision


def compute_MAP(ground_truth: dict, predicted_order: dict, k=None) -> float:
    """
    Compute Mean Average Precision (MAP).

    Args:
    ground_truth (dict): Dictionary containing the ground truth rankings.
    predicted_order (dict): Dictionary containing the predicted rankings.
    k (int): Number of items to consider for precision computation. Default is None (consider all items).

    Returns:
    map_score (float): Mean Average Precision (MAP) score.
    """
    precisions = []
    for query_id in ground_truth.keys():
        ground_truth_order = ground_truth[query_id]
        predicted_order_list = predicted_order.get(query_id, [])
        if k is not None:
            predicted_order_list = predicted_order_list[:k]
        precision_sum = sum(
            compute_precision_at_k(ground_truth_order, predicted_order_list, j + 1)
            for j in range(len(predicted_order_list))
        )
        avg_precision = (
            precision_sum / len(predicted_order_list)
            if (len(ground_truth_order) > 0 and len(predicted_order_list) > 0)
            else 0
        )
        precisions.append(avg_precision)
    map_score = np.mean(precisions)
    return map_score


def compute_RWP(ground_truth: dict, predicted_order: dict) -> float:
    """
    Compute Rank wise Precision (RWP).
    """
    reciprocal_ranks = []
    for query_id in ground_truth.keys():
        ground_truth_order = ground_truth[query_id]
        predicted_order_list = predicted_order.get(query_id, [])
        reciprocal_rank = 0
        for _, item in enumerate(predicted_order_list, start=1):
            if item in ground_truth_order:
                reciprocal_rank += 1 / len(predicted_order_list)

        reciprocal_ranks.append(reciprocal_rank)
    mrr_score = np.mean(reciprocal_ranks)
    return mrr_score


def compute_MRR(ground_truth: dict, predicted_order: dict) -> float:
    """
    Compute Mean Reciprocal Rank (MRR).

    Args:
    ground_truth (dict): Dictionary containing the ground truth rankings.
    predicted_order (dict): Dictionary containing the predicted rankings.

    Returns:
    mrr_score (float): Mean Reciprocal Rank (MRR) score.
    """
    reciprocal_ranks = []
    for query_id in ground_truth.keys():
        ground_truth_order = ground_truth[query_id]
        predicted_order_list = predicted_order.get(query_id, [])
        reciprocal_rank = 0
        for rank, item in enumerate(predicted_order_list, start=1):
            if item in ground_truth_order:
                reciprocal_rank += 1 / rank

        reciprocal_ranks.append(reciprocal_rank)
    mrr_score = np.mean(reciprocal_ranks)
    return mrr_score


def evaluate_rank(ground_truth: str, response: str, prompt: str, model):

    ground_truth = ground_truth.replace(",", "<")

    # For direct prompt
    if prompt != "d":
        prompt_part = []
        prompt_part.append(get_non_dec_order(response))
        response = gemini.send_request(model, prompt_part)
        # print(response)

    matches = re.findall(ANSWER_REGEX, response)

    if not matches:
        return None
    answer = matches[-1].strip()
    answer = replace_abbrev(answer)

    # For direct prompt
    if prompt == "d":
        answer = answer.replace(",", " > ")

    ground_ranks = parse_ranking_string(ground_truth)
    predicted_ranks = parse_ranking_string(answer)

    ground_list = flatten_ranks(ground_ranks)
    filtered_predicted_ranks = filter_items(ground_list, predicted_ranks)
    predicted_list = flatten_ranks(filtered_predicted_ranks)

    RHO = calculate_spearmanr_rho(ground_list, predicted_list)

    TAU = calculate_kendall_tau(ground_list, predicted_list)

    MRR = compute_MRR(ground_ranks, predicted_ranks)

    MAP = compute_MAP(ground_ranks, predicted_ranks)

    RWP = compute_RWP(ground_ranks, predicted_ranks)

    return RHO, TAU, MRR, MAP, RWP


def evaluate_single(ground_truth: str, response: str, country: str):

    ground_truth = " ".join(ground_truth.split())
    response = " ".join(response.split())

    if country == "india":
        ground_truth = ground_truth.lower().replace(
            "jammu and kashmir", "jammu & kashmir"
        )
        response = response.lower().replace("jammu and kashmir", "jammu & kashmir")

    ground_truth = ground_truth.lower()
    response = response.lower()

    ground_truth = ground_truth.replace(" and ", " , ")
    ground_truth = ground_truth.replace(" or ", " , ")

    response = response.replace(" and ", " , ")
    response = response.replace(" or ", " , ")

    exact_score = 0
    if ground_truth == response:
        exact_score = 1

    ground_list = ground_truth.split(",")
    response_list = response.split(",")

    ground_list = [item.strip() for item in ground_list]
    response_list = [item.strip() for item in response_list]

    full_score = 0
    partial_score = 0

    for resp_state in response_list:
        if resp_state in ground_list:
            full_score = 1
            partial_score += 1

    partial_score = partial_score / len(ground_list)

    return exact_score, full_score, partial_score


def isRelative(template):
    rel_template = ["22", "30", "32", "34", "35", "37", "38"]
    if template in rel_template:
        return True

    return False


def evaluate(json_data, country, prompt, model):
    global abbrev_dict
    global state_set

    if (
        country == "usa"
        or country == "usa_rank"
        or country == "jumb"
        or country == "shuff"
        or country == "orgs"
    ):
        abbrev_dict = US_STATES
    elif country == "india":
        abbrev_dict = INDIA_STATES
    elif country == "img":
        abbrev_dict = IMAGINARY_DICT
    elif country == "china":
        abbrev_dict = CHINA_STATES
    else:
        print("Not supported country")

    state_set = set(abbrev_dict.values())

    binary_total_count = 0
    binary_correct_count = 0

    single_total_count = 0
    single_exact_count = 0
    presence_single_score = 0
    partial_single_score = 0

    count_total_count = 0
    count_correct_count = 0

    range_total_count = 0
    range_correct_count = 0
    range_error_count = 0

    list_total_count = 0
    list_precision = 0
    list_recall = 0

    no_answer_cnt = 0
    rank_cnt = 0
    mrr_rank_score = 0
    new_mrr_rank_score = 0
    rho_rank_score = 0
    tau_rank_score = 0
    map_rank_score = 0
    correct_rank_cnt = 0

    cnt = 0
    for obj in tqdm(json_data, desc="Evaluating Responses"):
        cnt += 1

        ground_truth = obj["ground_truth"].strip()
        ground_truth_type = obj["ground_truth_type"]
        response = obj["response"]
        question = obj["question"]

        if (
            (r_yn == "y" and not isRelative(obj["template"]))
            or (r_yn == "n" and isRelative(obj["template"]))
            or (c_or_d == "d" and obj[c_or_d] == "c")
            or (c_or_d == "c" and obj[c_or_d] == "d")
        ):
            continue

        if not response:
            response = "None"
        matches = re.findall(ANSWER_REGEX, response)

        # No answer present
        if not matches:
            no_answer_cnt += 1
            print(ground_truth_type)
            if ground_truth_type == "Range":
                range_total_count += 1
            elif ground_truth_type == "List":
                list_total_count += 1
            elif ground_truth_type == "Binary":
                binary_total_count += 1
            elif ground_truth_type == "Single":
                single_total_count += 1
            elif ground_truth_type == "Count":
                count_total_count += 1
            continue

        answer = matches[-1].strip()
        answer = replace_abbrev(answer)

        if "Rank" in question or "rank" in question:

            rho, tau, mrr, map, rwp = evaluate_rank(
                ground_truth, response, prompt, model
            )
            mrr_rank_score += mrr
            rho_rank_score += rho
            tau_rank_score += tau
            map_rank_score += map
            new_mrr_rank_score += rwp
            if rwp == 1.0:
                correct_rank_cnt += 1
            rank_cnt += 1

        if ground_truth_type == "Range" or isRange(ground_truth):

            # Continue if the ground truth is not of type range
            if not (isRange(ground_truth) or has_digit(ground_truth)):
                continue
            try:
                score = evaluate_range(ground_truth, answer, obj["c_or_d"])
            except:
                range_error_count += 1
                score = 0
            range_correct_count += score

            range_total_count += 1

        elif ground_truth_type == "List":
            list_total_count += 1
            precision, recall = evaluate_list(ground_truth, answer, country)
            list_precision += precision
            list_recall += recall

        elif ground_truth_type == "Binary":
            if answer.lower() == ground_truth.lower():
                binary_correct_count += 1
            elif (answer.lower() == "false" and ground_truth.lower() == "no") or (
                answer.lower() == "True" and ground_truth.lower() == "yes"
            ):
                binary_correct_count += 1
            binary_total_count += 1

        elif ground_truth_type == "Single":
            single_total_count += 1
            exact_score, full_score, partial_score = evaluate_single(
                ground_truth, answer, country
            )

            single_exact_count += exact_score
            presence_single_score += full_score
            partial_single_score += partial_score

        elif ground_truth_type == "Count":
            if answer.lower() == ground_truth.lower():
                count_correct_count += 1
            count_total_count += 1

        if cnt == -1:
            break

    print("# no answer in the response - ", no_answer_cnt)

    print("# nunber of rank based questions - ", rank_cnt)

    if rank_cnt:
        print(f"Rho score - {rho_rank_score}/{rank_cnt} = {rho_rank_score/rank_cnt}")

        print(f"Tau score - {tau_rank_score}/{rank_cnt} = {tau_rank_score/rank_cnt}")

        print(f"MRR score - {mrr_rank_score}/{rank_cnt} = {mrr_rank_score/rank_cnt}")
        print(f"MAP score - {map_rank_score}/{rank_cnt} = {map_rank_score/rank_cnt}")
        print(
            f"RWP score - {new_mrr_rank_score}/{rank_cnt} = {new_mrr_rank_score/rank_cnt}"
        )

        print(
            f"correct ranking pred accuracy - {correct_rank_cnt}/{rank_cnt} = {correct_rank_cnt/rank_cnt}"
        )
    if binary_total_count:
        print(
            f"Binary Accuracy {binary_correct_count}/{binary_total_count} = {binary_correct_count/binary_total_count}"
        )
    else:
        print("# number of binary type qustions", 0)

    if single_total_count:
        print(
            f"Single Accuracy {single_exact_count}/{single_total_count} = {single_exact_count/single_total_count}"
        )

        print(
            f"Single Presence Score {presence_single_score}/{single_total_count} = {presence_single_score/single_total_count}"
        )

        print(
            f"Single Recall {partial_single_score}/{single_total_count} = {partial_single_score/single_total_count}"
        )
    else:
        print("# number of single type qustions", 0)

    if count_total_count:
        print(
            f"Count Accuracy {count_correct_count}/{count_total_count} = {count_correct_count/count_total_count}"
        )
    else:
        print("# number of count type qustions", 0)

    if range_total_count:
        print(f"Range Error Count {range_error_count}")

        print(
            f"Range Accuracy {range_correct_count}/{range_total_count} = {range_correct_count/range_total_count}"
        )
    else:
        print("# number of range type qustions", 0)

    if list_total_count:
        print(
            f"List Count {list_total_count}, precision {list_precision/list_total_count}, recall {list_recall/list_total_count}"
        )
    else:
        print("# number of list type qustions", 0)


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
        choices=["usa", "india", "china", "orgs", "img", "shuff", "jumb", "img"],
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
        "--c_or_d",
        type=str,
        default="_",
        choices=["y", "n"],
        help="c means continuos, d means discrete, o/w _",
    )

    parser.add_argument(
        "--r_yn",
        type=str,
        default="_",
        choices=["y", "n"],
        help="y means relative, n means non relative, o/w _",
    )

    # Parse the arguments
    args = parser.parse_args()

    model_name = args.model

    country_name = args.country
    map_type = args.map_type
    prompt_type = args.prompt

    c_or_d = args.c_or_d

    r_yn = args.r_yn

    if map_type == "wo":
        map_type = "wo_annotations"
    elif map_type == "w":
        map_type = "with_annotations"
    elif map_type == "h":
        map_type = "hatched"
    else:
        print("Wrong Map Type !")
        raise Exception("Wrong Map Type")

    response_file_dir = f"{responses_dir_path}/{model_name}/{country_name}/{map_type}/"
    response_filename = (
        response_file_dir + f"{country_name}_{map_type}_{prompt_type}_response.json"
    )

    with open(response_filename, "r") as file:
        json_data = json.load(file)

    print("Total responses to evaluate - ", len(json_data))
    print("***********************************")

    evaluate(json_data, country_name, prompt_type, gemini.get_gemini_model())
