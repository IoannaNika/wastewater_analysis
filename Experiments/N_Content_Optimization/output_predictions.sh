for n_content in 0.0 0.001 0.01 0.1; do \
  for ref_set in "Connecticut" "USA" "North_America" "Global"; do \
        bash ../../manuscript/run_kallisto_ref_sets_downsampling.sh ../../data/N_Content_Optimization/benchmarks/Connecticut 0 ../../data/N_Content_Optimization/reference_sets/${n_content}/${ref_set} 0.1 ${n_content}/${ref_set} B.1.1.7_sequence
    done
done