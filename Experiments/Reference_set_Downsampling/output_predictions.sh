for  seed in 1 2 3 4 5 6 7 8 9 10; do \
  for ref_set in "Netherlands" "Netherlands_nearby_countries" "Europe" "Global_next_regions"; do \
        bash ../../manuscript/run_kallisto_ref_sets_downsampling.sh ../Proximity_Experiments/Europe/Groningen/benchmarks/seed_1 0 reference_sets/${ref_set}/reference_set_${seed} 0.0 $ref_set/seed_${seed} B.1.1.7_sequence
    done
done