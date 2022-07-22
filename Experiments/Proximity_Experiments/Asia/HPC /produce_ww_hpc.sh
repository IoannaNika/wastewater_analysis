mkdir -p benchmarks
metadata="../../../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
sequences="../../../../../../GISAID/gisaid_2022_06_12/sequences.fasta"

for state in "Haryana" "Rajasthan" "West_Bengal"; do \
    mkdir -p benchmarks/$state 
    for seed in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
            mkdir -p benchmarks/$state/$seed
            python ../../../../benchmarking/create_benchmarks_with_seed.py --voc_perc 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100 -m $metadata -fr $sequences -fv ../../../../data/Proximity_Experiments/HPC/Asia/VOC_sequences/${state}/B.1.1.7_sequence.fasta -o benchmarks/${state}/$seed --total_cov 100 -s "Asia / India / ${state}" -d 2021-02-27 --seed $seed

        # cleanup intermediate files
        for file in benchmarks/$state/$seed/*; do \

            if ! [[ "$file"  =~ ^(benchmarks/$state/$seed/wwsim_|benchmarks/$state/$seed/metadata.tsv|benchmarks/$state/$seed/sequences.fasta).*$ ]]; 
            then 
            echo "$file is removed"
            rm $file
            fi
        done
    done
done