# build folder structure
mkdir reference_sets

for continent in "North_America" "Asia" "Europe"; do \
    mkdir reference_sets/$continent
done

for reference_set in \
"North_America/Connecticut ../../data/Proximity_Experiments/North_America/reference_sets/Connecticut/metadata.tsv ../../data/Proximity_Experiments/North_America/reference_sets/Connecticut/sequences.fasta" \
"North_America/Connecticut_nearby_states ../../data/Proximity_Experiments/North_America/reference_sets/Connecticut_nearby_states/metadata.tsv ../../data/Proximity_Experiments/North_America/reference_sets/Connecticut_nearby_states/sequences.fasta" \
"North_America/USA ../../data/Proximity_Experiments/North_America/reference_sets/USA/metadata.tsv ../../data/Proximity_Experiments/North_America/reference_sets/USA/sequences.fasta" \
"North_America/North_America ../../data/Proximity_Experiments/North_America/reference_sets/North_America/metadata.tsv ../../data/Proximity_Experiments/North_America/reference_sets/North_America/sequences.fasta" \
"North_America/Global_next_regions ../../data/Proximity_Experiments/North_America/reference_sets/Global_next_regions/metadata.tsv ../../data/Proximity_Experiments/North_America/reference_sets/Global_next_regions/sequences.fasta" \
"Europe/Netherlands ../../data/Proximity_Experiments/Europe/reference_sets/Netherlands/metadata.tsv ../../data/Proximity_Experiments/Europe/reference_sets/Netherlands/sequences.fasta" \
"Europe/Netherlands_nearby_countries ../../data/Proximity_Experiments/Europe/reference_sets/Netherlands_nearby_countries/metadata.tsv ../../data/Proximity_Experiments/Europe/reference_sets/Netherlands_nearby_countries/sequences.fasta" \
"Europe/Europe ../../data/Proximity_Experiments/Europe/reference_sets/Europe/metadata.tsv ../../data/Proximity_Experiments/Europe/reference_sets/Europe/sequences.fasta" \
"Europe/Global_next_regions ../../data/Proximity_Experiments/Europe/reference_sets/Global_next_regions/metadata.tsv ../../data/Proximity_Experiments/Europe/reference_sets/Global_next_regions/sequences.fasta" \
"Asia/Maharashtra ../../data/Proximity_Experiments/Asia/reference_sets/Maharashtra/metadata.tsv ../../data/Proximity_Experiments/Asia/reference_sets/Maharashtra/sequences.fasta" \
"Asia/Maharashtra_nearby_states ../../data/Proximity_Experiments/Asia/reference_sets/Maharashtra_nearby_states/metadata.tsv ../../data/Proximity_Experiments/Asia/reference_sets/Maharashtra_nearby_states/sequences.fasta" \
"Asia/India ../../data/Proximity_Experiments/Asia/reference_sets/India/metadata.tsv ../../data/Proximity_Experiments/Asia/reference_sets/India/sequences.fasta" \
"Asia/Asia ../../data/Proximity_Experiments/Asia/reference_sets/Asia/metadata.tsv ../../data/Proximity_Experiments/Asia/reference_sets/Asia/sequences.fasta" \
"Asia/Global_next_regions ../../data/Proximity_Experiments/Asia/reference_sets/Global_next_regions/metadata.tsv ../../data/Proximity_Experiments/Asia/reference_sets/Global_next_regions/sequences.fasta" ; do \
    #make tuples 
    IFS=' '
    set -- $reference_set 
    mkdir reference_sets/$1
    outpout_dir_main=reference_sets/$1
    #preprocess references
    python ../../pipeline/pipeline/preprocess_references.py -m $2 -f $3 --seed 0 -o $outpout_dir_main
    #calculate within lineage variation
    bash ../../pipeline/pipeline/call_variants.sh $outpout_dir_main /Users/ioanna/Projects/wastewater_analysis/data/Original_SARS-CoV-2_sequence/SARS-CoV-2-NC_045513.fasta

    for min_freq in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 ; do \
        outpout_dir=reference_sets/$1_$min_freq
        mkdir $outpout_dir
        # select samples
        python ../../pipeline/pipeline/select_samples.py -m $2 -f $3 -o $outpout_dir --vcf $outpout_dir_main/*_merged.vcf.gz --freq $outpout_dir_main/*_merged.frq --min_aaf $min_freq 
        #build kallisto index
        kallisto index -i $outpout_dir/sequences.kallisto_idx  $outpout_dir/sequences.fasta
    done 

    # remove everything except the metadata file, the fasta file, the lineage contents file & the kallisto index
    for file in ${outpout_dir_main}/*; do \
        if [[ -d "$file" ]] ; then
            echo "$file is a directory and it will be removed";
            rm -r $file
        elif ! [[ "$file"  =~ ^(${outpout_dir_main}/metadata.tsv|${outpout_dir_main}/sequences.kallisto_idx|${outpout_dir_main}/sequences.fasta|${outpout_dir_main}/lineages.txt)$ ]]; 
        then 
            echo "$file is removed"
            rm $file
        fi
    done


done



