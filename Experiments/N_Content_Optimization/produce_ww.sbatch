#!/bin/sh

#SBATCH --partition=general
#SBATCH --qos=long
#SBATCH --time=10:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=40960
#SBATCH --mail-type=END
#SBATCH --gres=gpu

bash produce_ww.sh
