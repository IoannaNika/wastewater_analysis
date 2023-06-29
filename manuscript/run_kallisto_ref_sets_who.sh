#!/bin/bash
#SBATCH -c 20
#SBATCH -t 0-5:00
#SBATCH -p short
#SBATCH --mem=20G
#SBATCH -o logs/run_kallisto_%j.out
#SBATCH -e logs/run_kallisto_%j.err

dataset=$1
num_bootstraps=$2
ref_dir=$3
min_ab=$4
out=$5
lineage_measured=$6

HDF5_USE_FILE_LOCKING=FALSE # prevent HDF5 problems (https://github.com/pachterlab/kallisto/issues/197)

outdir=kallisto_predictions_who/${out}
mkdir -p ${outdir}

for VOC in ${lineage_measured}; do \

  for ab in 1 2 3 4 5 6 7 8 9 10 20 30 40 50 60 70 80 90 100; do \
    /usr/bin/time -lp kallisto quant -t 8 -b ${num_bootstraps} -i ${ref_dir}/sequences.kallisto_idx -o ${outdir}/${VOC}_ab${ab} ${dataset}/wwsim_${VOC}_ab${ab}_1.fastq ${dataset}/wwsim_${VOC}_ab${ab}_2.fastq > ${outdir}/${VOC}_ab${ab}.log 2>&1;
    /usr/bin/time -lp python ../../../pipeline/pipeline/output_abundances.py --voc_file ../../../auxiliary_data/WHO_variants_2022-06-22.json -m $min_ab -o ${outdir}/${VOC}_ab${ab}/predictions_m${min_ab}.tsv --metadata ${ref_dir}/metadata.tsv ${outdir}/${VOC}_ab${ab}/abundance.tsv >> ${outdir}/${VOC}_ab${ab}.log 2>&1;
  done;
done;
