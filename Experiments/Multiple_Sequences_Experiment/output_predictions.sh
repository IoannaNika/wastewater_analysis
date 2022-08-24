for seed in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
  # Output predictions for a region in the Netherlands
  for ref_set in "Connecticut" "USA" "North_America" "Global"; do \
        bash ../../manuscript/run_kallisto_ref_sets_proximity_experiments.sh ../../data/Multiple_Sequences_Experiment/benchmarks/Connecticut/${seed} 0 ../../data/Proximity_Experiments/HPC/North_America/reference_sets/${ref_set} 0.1 Connecticut/${ref_set}/${seed} B.1.1.7_sequence
  done
done