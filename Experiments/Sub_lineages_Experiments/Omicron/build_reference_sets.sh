#!/bin/sh

metadata="../../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
sequences="../../../../../GISAID/gisaid_2022_06_12/sequences.fasta"

for state in "Connecticut"; do \
    outdir="reference_sets/$outdir"
    #make tuples 
    mkdir -p reference_sets
    mkdir -p $outdir
    # preprocess references
    python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 1 -o $outdir --state $state --startdate "2022-02-01" --enddate "2022-04-30"
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