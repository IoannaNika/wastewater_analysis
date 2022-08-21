# build folder structure

###############################################################

mkdir -p kallisto_predictions

for continent in "North_America" "Asia" "Europe"; do \
    mkdir -p kallisto_predictions/$continent
done

###############################################################

IFS=' '
# Predictions at lineage level
for datasets in \
"Asia/Maharashtra ../../../data/Proximity_Experiments/HPC/Asia/benchmarks/Maharashtra/1" \
"Asia/India ../../../data/Proximity_Experiments/HPC/Asia/benchmarks/Maharashtra/1" \
"Asia/Asia ../../../data/Proximity_Experiments/HPC/Asia/benchmarks/Maharashtra/1" \
"Asia/Global ../../../data/Proximity_Experiments/HPC/Asia/benchmarks/Maharashtra/1" \
"Europe/Netherlands ../../../data/Proximity_Experiments/HPC/Europe/benchmarks/Gelderland/1" \
"Europe/Europe ../../../data/Proximity_Experiments/HPC/Europe/benchmarks/Gelderland/1" \
"Europe/Global ../../../data/Proximity_Experiments/HPC/Europe/benchmarks/Gelderland/1" \
"North_America/Connecticut ../../../data/Proximity_Experiments/HPC/North_America/benchmarks/Connecticut/1" \
"North_America/USA ../../../data/Proximity_Experiments/HPC/North_America/benchmarks/Connecticut/1" \
"North_America/North_America ../../../data/Proximity_Experiments/HPC/North_America/benchmarks/Connecticut/1" \
"North_America/Global ../../../data/Proximity_Experiments/HPC/North_America/benchmarks/Connecticut/1" ; do \

  set -- $datasets
  mkdir -p kallisto_predictions/$1
  for  allele_freq in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0; do \
    bash ../../../manuscript/run_kallisto_ref_sets_downsampling.sh $2 0 ../../../data/Allele_Frequency_Optimization/reference_sets/$1_${allele_freq} 0.1 ${1}/${allele_freq} B.1.1.7_sequence
  done
done

###############################################################

# Predictions at VOC level
mkdir -p kallisto_predictions_who

for datasets in \
"Asia/Maharashtra ../../../data/Proximity_Experiments/HPC/Asia/benchmarks/Maharashtra/1" \
"Asia/India ../../../data/Proximity_Experiments/HPC/Asia/benchmarks/Maharashtra/1" \
"Asia/Asia ../../../data/Proximity_Experiments/HPC/Asia/benchmarks/Maharashtra/1" \
"Asia/Global ../../../data/Proximity_Experiments/HPC/Asia/benchmarks/Maharashtra/1" \
"Europe/Netherlands ../../../data/Proximity_Experiments/HPC/Europe/benchmarks/Gelderland/1" \
"Europe/Europe ../../../data/Proximity_Experiments/HPC/Europe/benchmarks/Gelderland/1" \
"Europe/Global ../../../data/Proximity_Experiments/HPC/Europe/benchmarks/Gelderland/1" \
"North_America/Connecticut ../../../data/Proximity_Experiments/HPC/North_America/benchmarks_who/benchmarks/Connecticut/1" \
"North_America/USA ../../../data/Proximity_Experiments/HPC/North_America/benchmarks_who/benchmarks/Connecticut/1" \
"North_America/North_America ../../../data/Proximity_Experiments/HPC/North_America/benchmarks_who/benchmarks/Connecticut/1" \
"North_America/Global ../../../data/Proximity_Experiments/HPC/North_America/benchmarks_who/benchmarks/Connecticut/1" ; do \

  set -- $datasets
  for  allele_freq in 0.0; do \
    bash ../../../manuscript/run_kallisto_ref_sets_who.sh $2 0 ../../../data/Allele_Frequency_Optimization/reference_sets/$1_${allele_freq} 0.1 ${1}/${allele_freq} B.1.1.7_sequence
  done
done


###############################################################
