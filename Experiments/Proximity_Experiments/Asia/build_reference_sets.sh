mkdir reference_sets

for reference_set in \
"Kerala ../../../data/Proximity_Experiments/Asia/reference_sets/Kerala/metadata.tsv ../../../data/Proximity_Experiments/Asia/reference_sets/Kerala/sequences.fasta" \
"Kerala_nearby_states ../../../data/Proximity_Experiments/Asia/reference_sets/Kerala_nearby_states/metadata.tsv ../../../data/Proximity_Experiments/Asia/reference_sets/Kerala_nearby_states/sequences.fasta" \
"Telangana ../../../data/Proximity_Experiments/Asia/reference_sets/Telangana/metadata.tsv ../../../data/Proximity_Experiments/Asia/reference_sets/Telangana/sequences.fasta" \
"Telangana_nearby_states ../../../data/Proximity_Experiments/Asia/reference_sets/Telangana_nearby_states/metadata.tsv ../../../data/Proximity_Experiments/Asia/reference_sets/Telangana_nearby_states/sequences.fasta" \
"Maharashtra ../../../data/Proximity_Experiments/Asia/reference_sets/Maharashtra/metadata.tsv ../../../data/Proximity_Experiments/Asia/reference_sets/Maharashtra/sequences.fasta" \
"Maharashtra_nearby_states ../../../data/Proximity_Experiments/Asia/reference_sets/Maharashtra_nearby_states/metadata.tsv ../../../data/Proximity_Experiments/Asia/reference_sets/Maharashtra_nearby_states/sequences.fasta" \
"India ../../../data/Proximity_Experiments/Asia/reference_sets/India/metadata.tsv ../../../data/Proximity_Experiments/Asia/reference_sets/India/sequences.fasta" \
"Asia ../../../data/Proximity_Experiments/Asia/reference_sets/Asia/metadata.tsv ../../../data/Proximity_Experiments/Asia/reference_sets/Asia/sequences.fasta" \
"Global_next_regions ../../../data/Proximity_Experiments/Asia/reference_sets/Global_next_regions/metadata.tsv ../../../data/Proximity_Experiments/Asia/reference_sets/Global_next_regions/sequences.fasta" ; do \
    #make tuples 
    set -- $reference_set 

    mkdir reference_sets/$1
    # preprocess references
    python ../../../pipeline/pipeline/preprocess_references.py -m $2 -f $3 --seed 0 -o reference_sets/$1
    # calculate within lineage variation
    bash ../../../pipeline/pipeline/call_variants.sh reference_sets/$1 /Users/ioanna/Projects/CSE3000_wastewater_project/data/SARS-CoV-2-NC_045513.fasta
    # select samples
    python ../../../pipeline/pipeline/select_samples.py -m $2 -f $3 -o reference_sets/$1 --vcf reference_sets/$1/*_merged.vcf.gz --freq reference_sets/$1/*_merged.frq

    #build kallisto index
    kallisto index -i reference_sets/$1/sequences.kallisto_idx  reference_sets/$1/sequences.fasta

    # remove everything except the metadata file, the fasta file, the lineage contents file & the kallisto index

    for file in reference_sets/$1/*; do \

        if [ -d "$file" ] ; then
            echo "$file is a directory and it will be removed";
            rm -r $file
        fi

        if ! [[ "$file"  =~ ^(reference_sets/$1/metadata.tsv|reference_sets/$1/sequences.kallisto_idx|reference_sets/$1/sequences.fasta|reference_sets/$1/lineages.txt)$ ]]; 
        then 
            echo "$file is removed"
            rm $file
        fi
    done

done
