#!/bin/sh
sequences="../../../../../GISAID/gisaid_2022_06_12/sequences.fasta"
start_date="2021-01-01"
end_date="2021-03-31"


for location_info in "Connecticut,state,Connecticut" "USA,country,USA" "North America,continent,North_America" "Global,all,Global"; do \
    IFS=','
    set -- $location_info
    location=$1
    location_type=$2
    folder_name=$3
    outdir=reference_sets/$folder_name

    for seed in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
        outdir=reference_sets/$folder_name
        metadata=$outdir/metadata_filtered_${seed}.tsv
        outdir=reference_sets/$folder_name/$seed

        # preprocess references
        python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o ${outdir} --startdate $start_date --enddate $end_date
        # calculate within lineage variation
        bash ../../../pipeline/pipeline/call_variants.sh ${outdir} /tudelft.net/staff-umbrella/SARSCoV2Wastewater/inika/wastewater_analysis/data/Original_SARS-CoV-2_sequence/SARS-CoV-2-NC_045513.fa
        # select samples
        python ../../../pipeline/pipeline/select_samples.py -m $metadata -f $sequences -o ${outdir} --vcf ${outdir}/*_merged.vcf.gz --freq ${outdir}/*_merged.frq

        #build kallisto index
        kallisto index -i ${outdir}/sequences.kallisto_idx  ${outdir}/sequences.fasta

        # remove everything except the metadata file, the fasta file, the lineage contents file & the kallisto index
        for file in ${outdir}/*; do \
            if [[ -d "$file" ]] ; then
                echo "$file is a directory and it will be removed";
                rm -r $file
            elif ! [[ "$file"  =~ ^(${outdir}/metadata.tsv|${outdir}/sequences.kallisto_idx|${outdir}/sequences.fasta|${outdir}/lineages.txt)$ ]]; 
            then 
                echo "$file is removed"
                rm $file
            fi
        done
    done
done

