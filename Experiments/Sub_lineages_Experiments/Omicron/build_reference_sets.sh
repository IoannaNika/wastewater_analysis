#!/bin/sh

metadata="../../../../../GISAID/gisaid_2022_08_18/metadata.tsv"
sequences="../../../../../GISAID/gisaid_2022_08_18/sequences.fasta"
start_date="2022-02-01"
end_date="2022-04-30"
IFS=','
mkdir -p reference_sets

for location_info in "Connecticut,Connecticut,state" "USA,USA,country" "North America,North_America,continent" "Global,Global,all"; do \ 
    #make tuples
    set -- $location_info
    location=$1
    folder_name=$2
    location_type=$3

    outdir=reference_sets/$folder_name
    mkdir -p $outdir

    if [[ "$location_type" == "all" ]] ; then
    # preprocess references
        python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o $outdir --startdate $start_date --enddate $end_date 
    elif [[ "$location_type" == "continent" ]] ; then
    # preprocess references
    python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o $outdir --startdate $start_date --enddate $end_date --continent $location 

    elif [[ "$location_type" == "country" ]] ; then
    # preprocess references
        python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o $outdir --startdate $start_date --enddate $end_date --country $location 

    else [[ "$location_type" == "state" ]]
    # preprocess references
        python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o $outdir --startdate $start_date --enddate $end_date --state $location
    fi 
    
    # calculate within lineage variation
    bash ../../../pipeline/pipeline/call_variants.sh $outdir /tudelft.net/staff-umbrella/SARSCoV2Wastewater/inika/wastewater_analysis/data/Original_SARS-CoV-2_sequence/SARS-CoV-2-NC_045513.fa
    # select samples
    python ../../../pipeline/pipeline/select_samples.py -m $metadata -f $sequences -o $outdir --vcf $outdir/*_merged.vcf.gz --freq $outdir/*_merged.frq --min_aaf 0.1

    #build kallisto index
    kallisto index -i $outdir/sequences.kallisto_idx  $outdir/sequences.fasta

    # remove intermidiate files and directories
     for file in $outdir/*; do \

            if [ -d "$file" ] ; then
                echo "$file is a directory and it will be removed";
                rm -r $file
            elif ! [[ "$file"  =~ ^($outdir/metadata.tsv|$outdir/sequences.kallisto_idx|$outdir/sequences.fasta|$outdir/lineages.txt)$ ]]; then 
                echo "$file is removed"
                rm $file
            fi
        done
done