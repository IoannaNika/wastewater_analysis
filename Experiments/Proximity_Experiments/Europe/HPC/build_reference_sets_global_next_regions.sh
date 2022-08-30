mkdir reference_sets

for reference_set in \
"Global_next_regions ../../../../data/Proximity_Experiments/HPC/Europe/reference_sets/Global_next_regions/metadata.tsv ../../../../data/Proximity_Experiments/HPC/Europe/reference_sets/Global_next_regions/sequences.fasta" ; do \
    #make tuples 
    set -- $reference_set 

    mkdir reference_sets/$1
    # preprocess references
    python ../../../../manuscript/preprocess_references_v1.py -m $2 -f $3 --seed 0 -o reference_sets/$1
    # calculate within lineage variation
    bash ../../../../pipeline/pipeline/call_variants.sh reference_sets/$1 /Users/ioanna/Projects/CSE3000_wastewater_project/data/SARS-CoV-2-NC_045513.fasta
    # select samples
    python ../../../../manuscript/select_samples_v1.py -m $2 -f $3 -o reference_sets/$1 --vcf reference_sets/$1/*_merged.vcf.gz --freq reference_sets/$1/*_merged.frq

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
