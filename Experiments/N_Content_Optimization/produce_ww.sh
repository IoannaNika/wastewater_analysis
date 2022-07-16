mkdir -p benchmarks
data="Connecticut"
mkdir -p benchmarks/$data
metadata="../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
sequences="../../../../GISAID/gisaid_2022_06_12/sequences.fasta"
python ../../benchmarking/create_benchmarks.py --voc_perc 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100 -m $metadata -fr $sequences -fv ../../data/N_Content_Optimization/B.1.1.7_sequence.fasta -o benchmarks/${data} --total_cov 100 -s ${data} -d 2021-04-30

# cleanup intermidiate files
for file in benchmarks/$data/*; do \

    if ! [[ "$file"  =~ ^( benchmarks/${data}/wwsim_|benchmarks/${data}/metadata.tsv|benchmarks/${data}/sequences.fasta).*$ ]]; 
    then 
    echo "$file is removed"
    rm $file
    fi
done

