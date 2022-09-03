benchmarks="../../../data/Proximity_Experiments/HPC/North_America/benchmarks_who/benchmarks/Connecticut/1"

for  seed in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
  for ref_set in "Connecticut" "USA" "North_America" "Global" ; do \
    ref_path="../../../data/Reference_set_Downsampling/reference_sets/$ref_set/$seed"
    bash ../../../manuscript/run_kallisto_ref_sets_who.sh $benchmarks 0 $ref_path 0.1 $ref_set/${seed} B.1.1.7_sequence
  done
done