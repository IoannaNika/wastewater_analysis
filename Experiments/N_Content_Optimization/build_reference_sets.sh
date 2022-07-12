#!/bin/sh

mkdir -p reference_sets
IFS=','
for n_content in 0.0 0.001 0.01 0.1; do \
    mkdir -p reference_sets/$n_content
    for reference_set in "Connecticut,Connecticut,state"  "USA,USA,country" "North America,North_America,continent" "Global,Global,all"; do \
        
        #make tuples 
        set -- $reference_set 

        metadata="../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
        sequences="../../../../GISAID/gisaid_2022_06_12/sequences.fasta"
        location="$1" 
        folder_name=$2
        location_type=$3
        start_date="2021-01-01"
        end_date="2021-03-31"

        mkdir -p reference_sets/$n_content/$folder_name

        if [[ "$location_type" == "all" ]] ; then
            # preprocess references
            python ../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o reference_sets/$n_content/$folder_name --startdate $start_date --enddate $end_date --max_N_content $n_content
        elif [[ "$location_type" == "continent" ]] ; then
            # preprocess references
            python ../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o reference_sets/$n_content/$folder_name --startdate $start_date --enddate $end_date --continent $location --max_N_content $n_content
        
        elif [[ "$location_type" == "continent" ]] ; then
            # preprocess references
            python ../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o reference_sets/$n_content/$folder_name --startdate $start_date --enddate $end_date --country $location --max_N_content $n_content

        else [[ "$location_type" == "state" ]]
            # preprocess references
            python ../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o reference_sets/$n_content/$folder_name --startdate $start_date --enddate $end_date --state $location --max_N_content $n_content
        fi 

        # calculate within lineage variation
        bash ../../pipeline/pipeline/call_variants.sh reference_sets/$n_content/$folder_name /tudelft.net/staff-umbrella/SARSCoV2Wastewater/inika/wastewater_analysis/data/Original_SARS-CoV-2_sequence/SARS-CoV-2-NC_045513.fa
        # select samples
        python ../../pipeline/pipeline/select_samples.py -m $metadata -f $sequences -o reference_sets/$n_content/$folder_name --vcf reference_sets/$n_content/$folder_name/*_merged.vcf.gz --freq reference_sets/$n_content/$folder_name/*_merged.frq

        #build kallisto index
        kallisto index -i reference_sets/$n_content/$folder_name/sequences.kallisto_idx  reference_sets/$n_content/$folder_name/sequences.fasta

        # remove everything except the metadata file, the fasta file, the lineage contents file & the kallisto index

        for file in reference_sets/$n_content/$folder_name/*; do \

            if [ -d "$file" ] ; then
                echo "$file is a directory and it will be removed";
                rm -r $file
            fi

            if ! [[ "$file"  =~ ^(reference_sets/$n_content/$folder_name/metadata.tsv|reference_sets/$n_content/$folder_name/sequences.kallisto_idx|reference_sets/$n_content/$folder_name/sequences.fasta|reference_sets/$n_content/$folder_name/lineages.txt)$ ]]; 
            then 
                echo "$file is removed"
                rm $file
            fi
        done

    done
done
