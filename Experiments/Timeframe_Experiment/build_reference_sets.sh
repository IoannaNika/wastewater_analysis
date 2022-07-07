mkdir reference_sets

for dataset in "Asia" "Europe" "Asia" "Global" "North_America"; do \
echo $dataset
    mkdir reference_sets/${dataset}
    for start_date in "2020-01-01" "2021-01-01" "2021-06-01" "2022-01-01" "2022-06-01"; do \

        path="../../data/Timeframe_Experiments/reference_sets/${dataset}_next_regions_download_6_Jul_2022/${start_date}_till_2022-06-08"
        outdir="reference_sets/${dataset}/${start_date}_till_2022-06-08"
        # preprocess references
        mkdir ${outdir}
        python ../../pipeline/pipeline/preprocess_references.py -m ${path}/metadata.tsv -f ${path}/sequences.fasta --seed 0 -o ${outdir} --pango_lin pango_lineage
        # calculate within lineage variation
        bash ../../pipeline/pipeline/call_variants.sh ${outdir} /Users/ioanna/Projects/CSE3000_wastewater_project/data/SARS-CoV-2-NC_045513.fasta
        # select samples
        python ../../pipeline/pipeline/select_samples.py -m ${path}/metadata.tsv -f ${path}/sequences.fasta -o ${outdir} --vcf ${outdir}/*_merged.vcf.gz --freq ${outdir}/*_merged.frq --pango_lin pango_lineage

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

