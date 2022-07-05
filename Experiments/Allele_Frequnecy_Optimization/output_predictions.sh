# build folder structure
mkdir kallisto_predictions

for continent in "North_America" "Asia" "Europe"; do \
    mkdir kallisto_predictions/$continent
done

for datasets in \
"North_America/Connecticut ../Proximity_Experiments/North_America/Connecticut/benchmarks/seed_1" \
"North_America/Connecticut_nearby_states ../Proximity_Experiments/North_America/Connecticut/benchmarks/seed_1" \
"North_America/USA ../Proximity_Experiments/North_America/Connecticut/benchmarks/seed_1" \
"North_America/North_America ../Proximity_Experiments/North_America/Connecticut/benchmarks/seed_1" \
"North_America/Global_next_regions ../Proximity_Experiments/North_America/Connecticut/benchmarks/seed_1" \
"Europe/Netherlands ../Proximity_Experiments/Europe/Groningen/benchmarks/seed_1" \
"Europe/Netherlands_nearby_countries ../Proximity_Experiments/Europe/Groningen/benchmarks/seed_1" \
"Europe/Europe ../Proximity_Experiments/Europe/Groningen/benchmarks/seed_1" \
"Europe/Global_next_regions ../Proximity_Experiments/Europe/Groningen/benchmarks/seed_1" \
"Asia/Maharashtra ../Proximity_Experiments/Asia/Maharashtra/benchmarks/seed_1" \
"Asia/Maharashtra_nearby_states ../Proximity_Experiments/Asia/Maharashtra/benchmarks/seed_1" \
"Asia/India ../Proximity_Experiments/Asia/Maharashtra/benchmarks/seed_1" \
"Asia/Asia ../Proximity_Experiments/Asia/Maharashtra/benchmarks/seed_1" \
"Asia/Global_next_regions ../Proximity_Experiments/Asia/Maharashtra/benchmarks/seed_1" ; do \
  set -- $datasets
  mkdir kallisto_predictions/$1
  for  allele_freq in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 ; do \
    bash ../../manuscript/run_kallisto_ref_sets_downsampling.sh $2 0 reference_sets/$1_${allele_freq} 0.0 ${1}/${allele_freq} B.1.1.7_sequence
  done
done
