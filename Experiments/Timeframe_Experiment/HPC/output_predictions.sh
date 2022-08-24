end_date="2022-01-01"

for ref_set in "Connecticut" "USA"; do \
    set -- $data
    for start_date in "2020-01-01" "2020-06-01" "2021-01-01" "2021-06-01"; do \
        ref_set_path="../../../data/Timeframe_Experiments/HPC/reference_sets/$ref_set/${start_date}_till_${end_date}/processed"        
        bash ../../../manuscript/run_kallisto_ref_sets_downsampling.sh ../../../data/Timeframe_Experiments/HPC/benchmarks/Connecticut/1/ 0 $ref_set_path 0.1 $ref_set/${start_date}_till_${end_date} AY.103_sequence 
    done
done