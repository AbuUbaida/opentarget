#!/bin/bash
#SBATCH --time=0-07:00:00
#SBATCH --account=<your_comp_canada_acc>
#SBATCH --mem=32000M
#SBATCH --gpus-per-node=v100l:1
#SBATCH --cpus-per-task=4

nvidia-smi

module load python/3.10
module load cuda cudnn

virtualenv --no-download ~/envs/llama
source ~/envs/llama/bin/activate
pip install --no-index --upgrade pip

pip install --no-index -r ~/path_to_/requirements.txt
python ~/path_to_/prompting_llama.py
