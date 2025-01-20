import os
import pandas as pd

template_file_path = os.path.join(
    os.path.dirname(__file__), "dataset/final_template2.csv"
)

Us_file_path = os.path.join(
    os.path.dirname(__file__), "dataset/usa/final_us_cleaned8.csv"
)
India_file_path = os.path.join(
    os.path.dirname(__file__), "dataset/india/final_india_cleaned4.csv"
)
China_file_path = os.path.join(
    os.path.dirname(__file__), "dataset/china/final_china_cleaned3.csv"
)

img_file_path = os.path.join(
    os.path.dirname(__file__), "dataset/counter_factuals/img/img_data.csv"
)
jumb_file_path = os.path.join(
    os.path.dirname(__file__), "dataset/counter_factuals/jumb/jumb_data.csv"
)
orgs_file_path = os.path.join(
    os.path.dirname(__file__), "dataset/counter_factuals/orgs/orgs_data.csv"
)
shuff_file_path = os.path.join(
    os.path.dirname(__file__), "dataset/counter_factuals/shuff/shuff_data.csv"
)

actual_map_paths = os.path.join(os.path.dirname(__file__), "dataset")
counter_factual_map_paths = os.path.join(
    os.path.dirname(__file__), "dataset/counter_factuals"
)

responses_dir_path = os.path.join(os.path.dirname(__file__), "responses")
no_responses_dir_path = os.path.join(os.path.dirname(__file__), "no_responses")

env_dir_path = os.path.join(os.path.dirname(__file__), ".env")

cot_f2_example_image_path = os.path.join(
    os.path.dirname(__file__), "aus_wo_anno_choro_map2.png"
)

actual_map_dataset_folder_name = "dataset"
counter_factual_dataset_folder_name = "dataset/counter_factuals"

CACHE_DIR = "/scratch/general/vast/u1471428/mapwise_data/models_cache"


TEMPLATES_TO_DROP = [2, 4, 5]


MAX_RETRY = 5
RETRY_DELAY = 2
REQUEST_DELAY_FREE = 4
REQUEST_DELAY_PAID = 0.07


ANSWER_REGEX = r'\{\s*"answer"\s*:\s*"?(.*?)"?\s*\}'

# for getting arraw_sign, value and unit
ARROW_VALUE_UNIT_REGEX = r"([<>]?)(-?\d+(\.\d+)?)([KkMmBbTt%]?)"

# for checking '-' is a range symbol
HAS_DASH_REGEX = r"([<>]?-?\d+(\.\d+)?[KkMmBbTt%]?)(-)([<>]?-?\d+(\.\d+)?[KkMmBbTt%]?)"


US_STATES = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

CHINA_STATES = {
    "BJ": "Beijing",
    "TJ": "Tianjin",
    "HE": "Hebei",
    "SX": "Shanxi",
    "NM": "Inner Mongolia",
    "LN": "Liaoning",
    "JL": "Jilin",
    "HL": "Heilongjiang",
    "SH": "Shanghai",
    "JS": "Jiangsu",
    "ZJ": "Zhejiang",
    "AH": "Anhui",
    "FJ": "Fujian",
    "JX": "Jiangxi",
    "SD": "Shandong",
    "HA": "Henan",
    "HB": "Hubei",
    "HN": "Hunan",
    "GD": "Guangdong",
    "GX": "Guangxi",
    "HI": "Hainan",
    "CQ": "Chongqing",
    "SC": "Sichuan",
    "GZ": "Guizhou",
    "YN": "Yunnan",
    "XZ": "Tibet",
    "SN": "Shaanxi",
    "GS": "Gansu",
    "QH": "Qinghai",
    "NX": "Ningxia",
    "XJ": "Xinjiang",
    "TW": "Taiwan",
    "HK": "Hong Kong",
    "MO": "Macau",
}

INDIA_STATES = {
    "AN": "Andaman and Nicobar Islands",
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CH": "Chandigarh",
    "CT": "Chhattisgarh",
    "DN": "Dadra and Nagar Haveli and Daman and Diu",
    "DL": "Delhi",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JK": "Jammu & Kashmir",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "LA": "Ladakh",
    "LD": "Lakshadweep",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OD": "Odisha",
    "PB": "Punjab",
    "PY": "Puducherry",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TS": "Telangana",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "UK": "Uttarakhand",
    "WB": "West Bengal",
}

IMAGINARY_DICT = {
    "AQ": "Aquilis",
    "BE": "Bexley",
    "CI": "Cirrus",
    "DA": "Davina",
    "EL": "Eloria",
    "FO": "Folium",
    "GI": "Gibralta",
    "HY": "Hyporia",
    "IR": "Iridia",
    "JU": "Junara",
    "KI": "Kivara",
    "LA": "Lavara",
    "MO": "Moxie",
    "NA": "Nacara",
    "OP": "Opaline",
    "PA": "Pallax",
    "QU": "Quixote",
    "RU": "Rumina",
    "SE": "Seraphine",
    "TI": "Tivala",
    "UV": "Uvera",
    "VO": "Vorana",
    "WY": "Wysteria",
    "XI": "Xivia",
    "YA": "Yalora",
    "ZO": "Zolara",
    "AD": "Adoria",
    "BI": "Bivana",
    "CO": "Coraline",
    "DU": "Dulcet",
    "EV": "Evoria",
    "FE": "Fenara",
    "GL": "Glacia",
    "HA": "Halcyon",
    "IS": "Isolara",
    "JE": "Jevana",
    "KR": "Kryon",
    "LU": "Lunara",
    "MY": "Mystara",
    "NE": "Nexus",
    "OR": "Oriana",
    "PU": "Pulsera",
    "RA": "Ravia",
    "SI": "Sirona",
    "TE": "Terrana",
    "UL": "Ulanara",
    "VA": "Valara",
    "WI": "Wixalia",
    "XA": "Xanara",
    "YO": "Yolena",
}

SHUFFLED_DICT = {
    "AL": "MT",
    "AK": "MS",
    "AZ": "MD",
    "AR": "ID",
    "CA": "CA",
    "CO": "VA",
    "CT": "NE",
    "DE": "GA",
    "FL": "NJ",
    "GA": "KY",
    "HI": "NY",
    "ID": "MI",
    "IL": "IL",
    "IN": "AR",
    "IA": "SC",
    "KS": "RI",
    "KY": "HI",
    "LA": "MO",
    "ME": "OK",
    "MD": "AL",
    "MA": "UT",
    "MI": "ME",
    "MN": "ND",
    "MS": "WI",
    "MO": "TN",
    "MT": "NM",
    "NE": "NH",
    "NV": "MA",
    "NH": "MN",
    "NJ": "TX",
    "NM": "WA",
    "NY": "OR",
    "NC": "NC",
    "ND": "VT",
    "OH": "IN",
    "OK": "WY",
    "OR": "WV",
    "PA": "AZ",
    "RI": "NV",
    "SC": "PA",
    "SD": "CO",
    "TN": "OH",
    "TX": "CT",
    "UT": "FL",
    "VT": "IA",
    "VA": "KS",
    "WA": "LA",
    "WV": "AK",
    "WI": "DE",
    "WY": "SD",
}

if __name__ == "__main__":
    print(template_file_path)
    template_df = pd.read_csv(template_file_path)
    print(template_df.shape)
    print(os.path.dirname(__file__))
    print(actual_map_paths)
