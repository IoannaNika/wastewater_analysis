coverage=$1

for  seed in 1 ; do \
  for ref_set in "Global/reference_set"; do \
        bash ../../manuscript/run_kallisto_ref_sets_v1.sh benchmarks/seed_${seed}_${coverage}x 0 $ref_set 0.0 BA.3_sequence
    done
done
