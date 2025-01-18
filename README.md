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

