
python ../../benchmarking/create_benchmarks_multiple.py --div 13 --voc_perc 25 -m ../../data/Benchmark_Omicron_Main_Lineages/metadata.tsv -fr ../../data/Benchmark_Omicron_Main_Lineages/sequences.fasta -fv ../../data/BA.3_v2/BA.3_sequences.fasta -o benchmarks_global_v2/seed_${seed}_${coverage}x --total_cov ${coverage} --seed $seed 

