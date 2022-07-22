for n_content in 0.0 0.001 0.01 0.1; do \
  for ref_set in "Connecticut" "USA" "North_America" "Global"; do \
        bash ../../manuscript/run_kallisto_ref_sets_who.sh ../../data/N_Content_Optimization/benchmarks_who/benchmarks/Connecticut 0 ../../data/N_Content_Optimization/reference_sets/${n_content}/${ref_set} 0.1 ${n_content}/${ref_set} alpha_sequence
    done
done