
# benchmark="../../../data/Sublineages_Experiment/benchmarks/1"

# for ref_set in "Connecticut" "USA" "North_America" "Global"; do \
#   ref_dir="../../../data/Sublineages_Experiment/reference_sets/$ref_set"
#   bash ../../../manuscript/run_kallisto_ref_sets_downsampling.sh $benchmark 0 $ref_dir 0.1 $ref_set VOC_sequence_BA.2
#   done


benchmark="../../../data/Sublineages_Experiment/benchmarks_equal_ab_test"

for ref_set in "Connecticut" "USA" "North_America" "Global"; do \
  ref_dir="../../../data/Sublineages_Experiment/reference_sets/$ref_set"
  bash ../../../manuscript/run_kallisto_ref_set_sub_lineages_exp.sh $benchmark 0 $ref_dir 0.1 $ref_set
  done
