benchmarks="../../../data/Proximity_Experiments/HPC/North_America/benchmarks/Connecticut/1"

for  seed in 10; do \
  for ref_set in "Connecticut" "USA" "North_America" ; do \
    ref_path="../../../data/Reference_set_Downsampling/reference_sets/$ref_set/$seed"
    bash ../../../manuscript/run_kallisto_ref_sets_downsampling.sh $benchmarks 0 $ref_path 0.1 $ref_set/${seed} B.1.1.7_sequence
  done
done