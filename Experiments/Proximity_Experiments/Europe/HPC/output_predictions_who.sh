for seed in 11 12 13 14 15 16 17 18 19 20; do \
  # Output predictions for a region in the Netherlands
  for ref_set in "Netherlands" "Europe" "Global"; do \
        bash ../../../../manuscript/run_kallisto_ref_sets_proximity_experiments_who.sh ../../../../data/Proximity_Experiments/HPC/Europe/benchmarks/Gelderland/${seed} 0 ../../../../data/Proximity_Experiments/HPC/Europe/reference_sets/${ref_set} 0.1 Gelderland/${ref_set}/${seed} B.1.1.7_sequence
  done
  # Output predictions for a region in Spain
  for ref_set in "Spain" "Europe" "Global"; do \
        bash ../../../../manuscript/run_kallisto_ref_sets_proximity_experiments_who.sh ../../../../data/Proximity_Experiments/HPC/Europe/benchmarks/Madrid/${seed} 0 ../../../../data/Proximity_Experiments/HPC/Europe/reference_sets/${ref_set} 0.1 Madrid/${ref_set}/${seed} B.1.1.7_sequence
  done
  # Output predictions for a region in Estonia
  for ref_set in "Estonia" "Europe" "Global"; do \
        bash ../../../../manuscript/run_kallisto_ref_sets_proximity_experiments_who.sh ../../../../data/Proximity_Experiments/HPC/Europe/benchmarks/Northern_Estonia/${seed} 0 ../../../../data/Proximity_Experiments/HPC/Europe/reference_sets/${ref_set} 0.1 Northern_Estonia/${ref_set}/${seed} B.1.1.7_sequence
  done

done