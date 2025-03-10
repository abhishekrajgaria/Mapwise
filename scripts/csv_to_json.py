import os
import sys
import json
import math
import argparse
import pandas as pd


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from constants import *


def generateJsonData(
    df: pd.DataFrame, country_name: str, map_type: str, template_dict: dict
) -> list:
    """
    Converts QA pairs from csv to json list.
    Each row in the csv file include map_no, template_no, question, ground_truth, countinous or discrete, or Relative Region
    information. All these information alongside other computed information are stored in json object for
    easier trecking of everythin during execution and evaluation.
    """
    json_data = []
    num_discrepancies = 0
    num_None_answer = 0
    num_range_none = 0

    map_directory = f"{actual_map_paths}/{country_name}/{map_type}"
    if (
        country_name == "img"
        or country_name == "jumb"
        or country_name == "orgs"
        or country_name == "shuff"
    ):
        map_directory = (
            f"{counter_factual_dataset_folder_name}/{country_name}/{country_name}_maps/"
        )

    def getMapPath(map_no: str) -> str:
        map_path = map_directory + "/" + map_no + ".png"
        return map_path

    last_map_no = 0
    last_c_or_d = ""

    for i, row in df.iterrows():
        json_obj = {}

        if country_name == "usa":
            if not math.isnan(row.iloc[0]) and row.iloc[0] != last_map_no:
                last_map_no = row.iloc[0]
                last_c_or_d = row.iloc[5]

                if not isinstance(last_c_or_d, str):
                    last_c_or_d = ""
        elif (
            country_name == "img"
            or country_name == "jumb"
            or country_name == "orgs"
            or country_name == "shuff"
        ):
            last_map_no = row["map_no"]
            last_c_or_d = row["c_or_d"]
        else:  # for india and china
            last_map_no = row.iloc[0]
            last_c_or_d = last_map_no[-1].lower()

        template_no = int(row.iloc[1])
        question = str(row.iloc[2]).strip()

        if country_name == "usa":
            ground_truth = (
                "None" if not isinstance(row.iloc[4], str) else str(row.iloc[4]).strip()
            )
            c_or_d = last_c_or_d.strip()
            relative_region = (
                row.iloc[6].strip() if row.iloc[6] == "Y" or row.iloc[6] == "N" else ""
            )
        elif (
            country_name == "img"
            or country_name == "jumb"
            or country_name == "orgs"
            or country_name == "shuff"
        ):
            ground_truth = (
                "None"
                if not isinstance(row["verified answer"], str)
                else str(row["verified answer"]).strip()
            )
            c_or_d = last_c_or_d.strip()
            relative_region = (
                row["relative_region (y/n)"].strip()
                if row["relative_region (y/n)"] == "Y"
                or row["relative_region (y/n)"] == "N"
                else ""
            )
        elif country_name == "china":
            ground_truth = (
                "None" if not isinstance(row.iloc[3], str) else str(row.iloc[3]).strip()
            )
            c_or_d = last_c_or_d.strip()
            relative_region = (
                row.iloc[5].strip() if row.iloc[5] == "Y" or row.iloc[5] == "N" else ""
            )
        elif country_name == "india":
            ground_truth = (
                "None" if not isinstance(row.iloc[3], str) else str(row.iloc[3]).strip()
            )
            c_or_d = last_c_or_d.strip()
            relative_region = (
                row.iloc[4].strip() if row.iloc[4] == "Y" or row.iloc[4] == "N" else ""
            )

        ground_truth_type = template_dict[template_no]

        if ground_truth == "None":
            num_None_answer += 1

        if ground_truth_type == "Range":
            if ground_truth == "None":
                ground_truth = "N/A"
                num_range_none += 1

        if (
            country_name == "usa"
            or country_name == "img"
            or country_name == "jumb"
            or country_name == "shuff"
            or country_name == "orgs"
        ):
            map_no = "map_" + str(int(last_map_no))

        else:
            map_no = "map" + last_map_no

        map_path = getMapPath(map_no)

        json_obj = {
            "country": country_name,
            "map_type": map_type,
            "map_no": map_no,
            "map_path": map_path,
            "template_no": template_no,
            "question": question,
            "ground_truth": ground_truth,
            "ground_truth_type": ground_truth_type,
            "c_or_d": c_or_d,
            "relative_region": relative_region,
        }
        json_data.append(json_obj)

    print("None Count", num_None_answer)
    print("Num Range None", num_range_none)
    return json_data


def cleanDataFrame(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["question"])
    if "ground_truth" in df.columns:
        df["ground_truth"] = df["ground_truth"].fillna(value="None")

    if "verified answer" in df.columns:
        df["verified answer"] = df["verified answer"].fillna(value="None")
    return df


def checkColorShadPresence(question):
    if "color" in question or "colour" in question or "shad" in question:
        return True
    return False


def filter_data(json_data):
    """
    The method filters out QA object for Hatched Json dataset.
    TEMPLATES_TO_DROP are templates in which question involves colors, as hatched maps are black and white
    Also, only discrete type maps will be involved, hatched maps represent discrete information.
    """
    filter_data = []
    for obj in json_data:
        if obj["template_no"] not in TEMPLATES_TO_DROP and obj["c_or_d"] == "d":
            filter_data.append(obj)
    return filter_data


def filter_ranks(json_data):
    filter_data = []
    for obj in json_data:
        if obj["template_no"] == "43" or "Rank" in obj["question"]:
            filter_data.append(obj)
    return filter_data


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process some states and values.")

    # Add arguments
    parser.add_argument(
        "--country", type=str, required=True, help="The country to check"
    )

    parser.add_argument(
        "--map_type",
        type=str,
        required=True,
        help="Map Type",
    )

    # Parse the arguments
    args = parser.parse_args()

    country = args.country
    map_type = args.map_type
    # rank = True if args.rank else False

    if map_type == "wo":
        map_type = "wo_annotations"
    elif map_type == "w":
        map_type = "with_annotations"
    elif map_type == "h":
        map_type = "hatched"
    else:
        print("Wrong Map Type !")
        raise Exception("Wrong Map Type")

    template_df = pd.read_csv(template_file_path)
    template_df = template_df.rename(columns={"Unnamed: 0": "template_no"})
    template_df = template_df[["template_no", "Type"]]
    template_dict = template_df.set_index("template_no")["Type"].to_dict()
    df = None
    if country == "usa":
        df = pd.read_csv(Us_file_path)
    elif country == "orgs":
        df = pd.read_csv(orgs_file_path)
    elif country == "india":
        df = pd.read_csv(India_file_path)
    elif country == "china":
        df = pd.read_csv(China_file_path)
    elif country == "img":
        df = pd.read_csv(img_file_path)
    elif country == "jumb":
        df = pd.read_csv(jumb_file_path)
    elif country == "shuff":
        df = pd.read_csv(shuff_file_path)
    else:
        print("Country not supported")
        raise Exception(
            "Country not supported, Please try again from - usa, india, china, orgs, img, jumb, shuff"
        )

    dataset_dir_path = ""
    if country == "usa" or country == "india" or country == "china":
        dataset_dir_path = actual_map_paths
    else:
        dataset_dir_path = counter_factual_map_paths

    df = cleanDataFrame(df)

    json_data = generateJsonData(df, country, map_type, template_dict)

    if map_type == "hatched":
        hatched_path = f"./{country}/{map_type}"
        json_data = filter_data(json_data)

    os.makedirs(f"{dataset_dir_path}/{country}/json_data/", exist_ok=True)

    with open(
        f"{dataset_dir_path}/{country}/json_data/{country}_{map_type}_maps_data.json",
        "w",
    ) as file:
        json.dump(json_data, file, indent=4)

    print(len(json_data))
    print(f"{map_type} data saved!")
