mkdir -p benchmarks
metadata="../../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
sequences="../../../../../GISAID/gisaid_2022_06_12/sequences.fasta"
IFS=','
for info in "Noord-Holland,B.1.1.529,2022-02-10,Netherlands,Europe" "Connecticut,AY.103,2022-02-10,USA,North America" "Maharashtra,BA.1,2022-02-04,India,Asia"; do \
    set -- $info
    state=$1  
    folder_name=$1
    date=$3
    lineage=$2
    country=$4
    continent=$5
    mkdir -p benchmarks/$folder_name 
    for seed in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
            mkdir -p benchmarks/$folder_name/$seed
            
            python ../../../benchmarking/create_benchmarks_with_seed.py --voc_perc 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100 -m $metadata -fr $sequences -fv ../../../data/Timeframe_Experiments/HPC/VOCs/${state}/${lineage}_sequence.fasta -o benchmarks/${folder_name}/$seed --total_cov 100 -s "${continent} / ${country} / ${state}" -d $date --seed $seed

        # cleanup intermidiate files
        for file in benchmarks/$folder_name/$seed/*; do \

            if ! [[ "$file"  =~ ^(benchmarks/$folder_name/$seed/wwsim_|benchmarks/$folder_name/$seed/metadata.tsv|benchmarks/$folder_name/$seed/sequences.fasta).*$ ]]; 
            then 
            echo "$file is removed"
            rm $file
            fi
        done
    done
done