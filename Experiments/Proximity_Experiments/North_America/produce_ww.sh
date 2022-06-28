for benchmark_data_folder in "Connecticut" "Massachusetts" "Indiana"; do \
        mkdir $benchmark_data_folder/benchmarks
        for  seed in 1 2 3 4 5 6 7 8 9 10; do \
                python ../../../benchmarking/create_benchmarks_with_seed.py --voc_perc 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100 -m ../../../data/Proximity_Experiments/North_America/benchmarks/$benchmark_data_folder/metadata.tsv -fr ../../../data/Proximity_Experiments/North_America/benchmarks/$benchmark_data_folder/sequences.fasta -fv ../../../data/Proximity_Experiments/North_America/benchmarks/$benchmark_data_folder/B.1.1.7_sequence.fasta -o $benchmark_data_folder/benchmarks/seed_$seed --total_cov 100 --seed $seed

                # remove intermidiate files

                for file in $benchmark_data_folder/benchmarks/seed_$seed/*; do \

                if ! [[ "$file"  =~ ^($benchmark_data_folder/benchmarks/seed_$seed/wwsim_|$benchmark_data_folder/benchmarks/seed_$seed/metadata.tsv|$benchmark_data_folder/benchmarks/seed_$seed/sequences.fasta).*$ ]]; 
                then 
                echo "$file is removed"
                rm $file
                fi
                done
        done
done
