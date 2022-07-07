for data in "Belgium Europe" "Jakarta Asia" "Colorado North_America"; do \
    set -- $data
    for start_date in "2020-01-01" "2021-01-01" "2021-06-01" "2022-01-01" "2022-06-01"; do \
        ref_set_path="reference_sets/$2/${start_date}_till_2022-06-08"
        ref_st_global_path="reference_sets/Global/${start_date}_till_2022-06-08"
        bash ../../manuscript/run_kallisto_ref_sets_downsampling.sh benchmarks/$1 0 $ref_set_path 0.0 $1/$2/${start_date}_till_2022-06-08 BA.4_sequence 
        # output results for the global reference set
        bash ../../manuscript/run_kallisto_ref_sets_downsampling.sh benchmarks/$1 0 $ref_st_global_path 0.0 $1/Global/${start_date}_till_2022-06-08 BA.4_sequence 
    done
done