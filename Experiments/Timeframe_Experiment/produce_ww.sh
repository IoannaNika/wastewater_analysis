mkdir benchmarks

for data in "Belgium 14" "Jakarta 20" "Colorado 17"; do \
        set -- $data
        mkdir benchmarks/$1
        path="../../data/Timeframe_Experiments/benchmarks/${1}_2022-06-10_till_2022-06-30"
        python ../../benchmarking/create_benchmarks_multiple.py --voc_perc 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100 -m $path/metadata.tsv -fr $path/sequences.fasta -fv $path/BA.4_sequences.fasta -o benchmarks/$1 --div $2 --total_cov 100 --seed 1 


        # remove intermidiate files

        for file in  benchmarks/$1/*; do \

        if ! [[ "$file"  =~ ^(benchmarks/$1/wwsim_|benchmarks/$1/metadata.tsv|benchmarks/$1/sequences.fasta).*$ ]]; 
        then 
        echo "$file is removed"
        rm $file
        fi
        done
done
