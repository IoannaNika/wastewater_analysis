date="2022-07-01"
metadata="../../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
sequences="../../../../../GISAID/gisaid_2022_06_12/sequences.fasta"
seed=1
coverage=100
state="Connecticut"
voc="../../../data/Sublineages_Experiment/VOC/VOC_sequence_BA.5.5.fasta"
mkdir -p benchmarks
mkdir -p benchmarks/1

python ../../../benchmarking/create_benchmarks_with_seed.py --voc_perc 10 -m $metadata -fr $sequences -fv $voc -o benchmarks/${seed} --total_cov ${coverage} --seed $seed -s $state
