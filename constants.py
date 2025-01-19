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
    os.path.dirname(__file__), "dataset/counter_factual"
)

actual_map_dataset_folder = "dataset"
counter_factual_dataset_folder = "dataset/counter_factual"


TEMPLATES_TO_DROP = [2, 4, 5]

if __name__ == "__main__":
    print(template_file_path)
    template_df = pd.read_csv(template_file_path)
    print(template_df.shape)
    print(os.path.dirname(__file__))
    print(actual_map_paths)
