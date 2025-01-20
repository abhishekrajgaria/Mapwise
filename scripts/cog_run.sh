#!/bin/bash
#SBATCH --account soc-gpu-np
#SBATCH --partition soc-gpu-np
#SBATCH --ntasks-per-node=32
#SBATCH --nodes=1
#SBATCH --gres=gpu
#SBATCH --time=3:00:00
#SBATCH --mem=20GB
#SBATCH --mail-user=u1471428@utah.edu
#SBATCH --mail-type=FAIL,END
#SBATCH -o ../run_output/submit_-%j
#SBATCH --export=ALL
source ~/miniconda3/etc/profile.d/conda.sh
conda activate mapwise
python main.py --model=idefics --country=usa --map_type=wo --prompt=cot_z --sample_size=2