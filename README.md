# MAPWise: Evaluating Visioin-Language Models for Advanced Map Queries


## Setup
The code can be run under any environment with Python 3.8 and above. (It may run with lower version, but we haven't tested it)

We recommend using [Miniconda](https://docs.anaconda.com/miniconda/) and creating a conda environment

For installing Miniconda on the above link, right-click on a suitable installer and select “Copy Link Address”, then wget that link and installed the downloaded bash file. E.g,. on Linux 64-bit and python 3.8:

     wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.5.2-0-Linux-x86_64.sh

     bash Miniconda3-py38_23.5.2-0-Linux-x86_64.sh
- Accept the license
- Install miniconda into default location
- Initialize

Create and activate a test Conda environment with desired python version e.g., 3.8

     conda create-n mapwise python=3.8

     conda activate mapwise

Next Install the required packages:
     
     pip install -r requirements.txt


## Dataset Structure

- `dataset/`

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

    

    
