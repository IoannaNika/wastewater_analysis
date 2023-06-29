end_date="2022-01-01"

for ref_set in "Connecticut" "USA" "North_America"; do \
    # set -- $data
    for start_date in "2020-01-01" "2020-06-01" "2021-01-01" "2021-06-01"; do \

        for seed in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
            ref_set_path="reference_sets/$ref_set/${start_date}_till_${end_date}/processed"        
            bash ../../../manuscript/run_kallisto_ref_sets_downsampling.sh Connecticut/$seed/ 0 $ref_set_path 0.1 $ref_set/${start_date}_till_${end_date} AY.103_sequence 
        done
    done
done