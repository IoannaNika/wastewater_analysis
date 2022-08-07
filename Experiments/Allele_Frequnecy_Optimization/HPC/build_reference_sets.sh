# build folder structure
mkdir -p reference_sets

for continent in "North_America" "Asia" "Europe"; do \
    mkdir -p reference_sets/$continent
done

for reference_set in \
"North_America/Connecticut,2021-01-01,2021-03-31" \
"North_America/USA,2021-01-01,2021-03-31" \
"North_America/North_America,2021-01-01,2021-03-31" \
"North_America/Global,2021-01-01,2021-03-31" \
"Europe/Netherlands,2020-10-01,2020-12-31" \
"Europe/Europe,2020-10-01,2020-12-31" \
"Europe/Global,2020-10-01,2020-12-31" \
"Asia/Maharashtra,2020-11-01,2021-01-31" \
"Asia/India,2020-11-01,2021-01-31" \
"Asia/Asia,2020-11-01,2021-01-31" \
"Asia/Global,2020-11-01,2021-01-31" ; do \
    
    metadata="../../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
    sequences="../../../../../GISAID/gisaid_2022_06_12/sequences.fasta"
    
    #make tuples 
    IFS=','
    set -- $reference_set 
    mkdir -p reference_sets/$1
    outpout_dir_main=reference_sets/$1
    start_date=$2
    end_date=$3
    #preprocess references
    python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o $outpout_dir_main --startdate $start_date --enddate $end_date

    #calculate within lineage variation
    bash ../../../pipeline/pipeline/call_variants.sh $outpout_dir_main /Users/ioanna/Projects/wastewater_analysis/data/Original_SARS-CoV-2_sequence/SARS-CoV-2-NC_045513.fasta

    for min_freq in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 ; do \
        outpout_dir=reference_sets/$1_$min_freq
        mkdir -p $outpout_dir
        # select samples
        python ../../../pipeline/pipeline/select_samples.py -m $metadata -f $sequences -o $outpout_dir --vcf $outpout_dir_main/*_merged.vcf.gz --freq $outpout_dir_main/*_merged.frq --min_aaf $min_freq 
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



