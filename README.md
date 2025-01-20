# MAPWise: Evaluating Visioin-Language Models for Advanced Map Queries


## Setup
The code can be run under any environment with Python 3.9 and above.

We recommend using [Miniconda](https://docs.anaconda.com/miniconda/) and creating a conda environment

For installing Miniconda on the above link, right-click on a suitable installer and select “Copy Link Address”, then wget that link and installed the downloaded bash file. E.g,. on Linux 64-bit and python 3.9:

     wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.5.2-0-Linux-x86_64.sh

     bash Miniconda3-py38_23.5.2-0-Linux-x86_64.sh
- Accept the license
- Install miniconda into default location
- Initialize

Create and activate a test Conda environment with desired python version e.g., 3.9

     conda create-n mapwise python=3.9

     conda activate mapwise

Next Install the required packages:
     
     pip install -r requirements.txt

> **Note**: The `requirements.txt` file may be incomplete. If you encounter any missing dependencies while running the scripts, install them using `pip install <package-name>` and then update the `requirements.txt` file by running:
   > ```bash
   > pip freeze > requirements.txt
   > ```

Create a `.env` file in the root directory of the project. This file should contain the necessary credentials for the project, including:
    
    GEMINI_API_KEY = your_gemini_api_key
    OPENAI_API_KEY = your_openai_api_key
    


## Dataset Structure

- `dataset/`
    - `final_template.csv`
    - `india/`
        - `hatched/` (55 files)
        - `metadata/` (109 files)
        - `with_annotations/` (110 files)
        - `wo_annotations/` (110 files)
        - `final_india_cleaned.csv`

    - `china/`
        - `hatched/` (51 files)
        - `metadata/` (100 files)
        - `with_annotations/` (100 files)
        - `wo_annotations/` (100 files)
        - `final_china_cleaned.csv`
    
    - `usa/`
        - `hatched/` (81 files)
        - `metadata/` (120 files)
        - `original_maps/` (120 files)
        - `with_annotations/` (120 files)
        - `wo_annotations/` (120 files)
        - `final_us_cleaned.csv`

    - `counter_factuals/`
        - `img/`
            - `img_maps/` (120 files)
            - `img_data.csv`
        - `jumb/`
            - `jumb_maps/` (120 files)
            - `jumb_data.csv`
        - `orgs/`
            - `orgs_maps/` (120 files)
            - `orgs_data.csv`
        - `shuff/`
            - `shuff_maps/` (120 files)
            - `shuff_data.csv`

## Running Models

### Overview

This `main.py` script processes map-related data for various models and generates structured responses. It supports multiple models, countries, and map types, with options to customize the input prompts and shuffle or sample the dataset.

Usage

Run the script using the command line:

```bash
python main.py --model <MODEL> --country <COUNTRY> --map_type <MAP_TYPE> --prompt <PROMPT> [--random] [--sample_size <SIZE>]
```
### Arguments

| Argument       | Type   | Required | Choices                                                                                       | Description                                                                                   |
|----------------|--------|----------|-----------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| `--model`      | String | Yes      | `gemini`, `gpt4`, `cog`, `idefics`, `internlm`, `qwen`                                       | Specifies the model to use.                                                                  |
| `--country`    | String | Yes      | `usa`, `india`, `china`, `orgs`, `img`, `shuff`                                              | The country or data category to process.                                                     |
| `--map_type`   | String | Yes      | `w`, `wo`, `h`                                                                               | Specifies the type of map to process: `w` (with annotations), `wo` (without annotations), or `h` (hatched). |
| `--prompt`     | String | Yes      | `d`, `cot_z`, `cot_f`, `cot_f2`, `eer`                                                      | Specifies the prompt type for the model.                                                     |
| `--random`     | Flag   | No       | None                                                                                         | Shuffles the dataset if specified.                                                           |
| `--sample_size`| Int    | No       | Any positive integer                                                                         | Limits the number of records to process. Default is `-1` (process all records).              |

    
## Scripts

### `csv_to_json.py`

Our original question answer data was captured and stored in csv format, but for efficient use and consistency we convert it to a json array format. (We recommend directly using the json data only)\
It takes two parameters --country and --map_type \
country could be {'usa', 'india', 'china', 'orgs', 'jumb', 'shuff','img'}
- orgs - original maps with annotation from usa dataset which are used to create counterfactual maps.
- jumb - counterfactual maps in which the values are altered.
- shuff - counterfactual maps in which the position of states are shuffled.
- img - counterfactual maps in which the name of states are replaced with imaginary names.

map_type = {wo, w, h}
- wo - maps without annotation
- w - maps with annotation
- h - hatched maps

To run for actual maps you could choose country from {'usa', 'india', 'china'} and map_type form {wo, w, h}, e.g., 

    python csv_to_json.py --country=usa --map_type=wo

For counterfactual maps you could choose country from {'orgs', 'jumb', 'shuff','img'} and map_type from {w}, e.g.,

    python csv_to_json.py --country=shuff --map_type=w

    
