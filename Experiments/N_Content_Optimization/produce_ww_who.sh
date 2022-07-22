mkdir -p benchmarks_who
data="Connecticut"
mkdir -p benchmarks_who/$data
metadata="../../data/N_Content_Optimization/benchmarks_who/Connecticut/metadata.tsv"
sequences="../../data/N_Content_Optimization/benchmarks_who/Connecticut/sequences.fasta"
python ../../benchmarking/create_benchmarks.py --voc_perc 1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100 -m $metadata -fr $sequences -fv ../../data/N_Content_Optimization/VOC_sequence/alpha_sequence.fasta -o ../../../../data/N_Content_Optimization/benchmarks_who/benchmarks/${data} --total_cov 100 -s "North America / USA / ${data}" -d 2021-04-30

# cleanup intermidiate files
for file in benchmarks_who/$data/*; do \

    if ! [[ "$file"  =~ ^(benchmarks_who/${data}/wwsim_|benchmarks_who/${data}/metadata.tsv|benchmarks_who/${data}/sequences.fasta).*$ ]]; 
    then 
    echo "$file is removed"
    rm $file
    fi
done

