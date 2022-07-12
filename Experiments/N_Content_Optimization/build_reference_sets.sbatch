#!/bin/sh

#SBATCH --partition=general
#SBATCH --qos=short
#SBATCH --time=8:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=10000
#SBATCH --mail-type=END
#SBATCH --gres=gpu

srun bash build_reference_sets.sh
