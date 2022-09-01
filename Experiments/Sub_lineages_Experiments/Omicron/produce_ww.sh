
metadata="../../../../../GISAID/gisaid_2022_08_18/metadata.tsv"
sequences="../../../../../GISAID/gisaid_2022_08_18/sequences.fasta"
seed=1
coverage=100
state="Connecticut"
date="2022-05-31"
voc="../../../data/Sublineages_Experiment/VOC/VOC_sequence_BA.2.fasta"
mkdir -p benchmarks
mkdir -p benchmarks/$seed

python ../../../benchmarking/create_benchmarks_with_seed.py --voc_perc 1 -m $metadata -fr $sequences -fv $voc -o benchmarks/${seed} --total_cov ${coverage} --seed $seed -s "North America / USA / ${state}" -d $date
