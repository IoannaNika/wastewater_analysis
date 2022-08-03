mkdir -p benchmarks
metadata="../../../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
sequences="../../../../../../GISAID/gisaid_2022_06_12/sequences.fasta"

IFS=','
for state in "Haryana,Haryana,2021-02-27" "Maharashtra,Maharashtra,2021-03-01" "Delhi,Delhi,2021-03-01"; do \
    set -- $state
    folder_name=$1
    state=$2
    date=$3
    mkdir -p benchmarks/$folder_name 
    for seed in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
            mkdir -p benchmarks/$folder_name/$seed
            python ../../../../benchmarking/create_benchmarks_with_seed.py --voc_perc 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100 -m $metadata -fr $sequences -fv ../../../../data/Proximity_Experiments/HPC/Asia/VOC_sequences/${folder_name}/B.1.1.7_sequence.fasta -o benchmarks/${folder_name}/$seed --total_cov 100 -s "Asia / India / ${state}" -d $date --seed $seed

        # cleanup intermediate files
        for file in benchmarks/$folder_name/$seed/*; do \

            if ! [[ "$file"  =~ ^(benchmarks/$folder_name/$seed/wwsim_|benchmarks/$folder_name/$seed/metadata.tsv|benchmarks/$folder_name/$seed/sequences.fasta).*$ ]]; 
            then 
            echo "$file is removed"
            rm $file
            fi
        done
    done
done