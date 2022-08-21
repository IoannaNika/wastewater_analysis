# build folder structure
mkdir -p reference_sets

for continent in "North_America" "Asia" "Europe"; do \
    mkdir -p reference_sets/$continent
done

for reference_set in \
"North_America/Connecticut,2021-01-01,2021-03-31,Connecticut,state" \
"North_America/USA,2021-01-01,2021-03-31,USA,country" \
"North_America/North_America,2021-01-01,2021-03-31,North America,continent" \
"North_America/Global,2021-01-01,2021-03-31,Global,all" \
"Europe/Netherlands,2020-10-01,2020-12-31,Netherlands,country" \
"Europe/Europe,2020-10-01,2020-12-31,Europe,continent" \
"Europe/Global,2020-10-01,2020-12-31,Global,all" \
"Asia/Maharashtra,2020-11-01,2021-01-31,Maharashtra,state" \
"Asia/India,2020-11-01,2021-01-31,India,country" \
"Asia/Global,2020-11-01,2021-01-31,Global,all" \
"Asia/Asia,2020-11-01,2021-01-31,Asia,continent" ; do \
    
    metadata="../../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
    sequences="../../../../../GISAID/gisaid_2022_06_12/sequences.fasta"
    
    #make tuples 
    IFS=','
    set -- $reference_set 
    mkdir -p reference_sets/$1
    outpout_dir_main=reference_sets/$1
    location=$4
    location_type=$5
    start_date=$2
    end_date=$3
    #preprocess references
    if [[ "$location_type" == "state" ]] ; then
        python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o $outpout_dir_main --startdate $start_date --enddate $end_date  --state $location
    fi 

    if [[ "$location_type" == "country" ]] ; then
        python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o $outpout_dir_main --startdate $start_date --enddate $end_date  --country $location
    fi

    if [[ "$location_type" == "continent" ]] ; then
        python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o $outpout_dir_main --startdate $start_date --enddate $end_date  --continent $location
    fi  

    if [[ "$location_type" == "all" ]] ; then
        python ../../../pipeline/pipeline/preprocess_references.py -m $metadata -f $sequences --seed 0 -o $outpout_dir_main --startdate $start_date --enddate $end_date
    fi  
    #calculate within lineage variation
    bash ../../../pipeline/pipeline/call_variants.sh $outpout_dir_main /tudelft.net/staff-umbrella/SARSCoV2Wastewater/inika/wastewater_analysis/data/Original_SARS-CoV-2_sequence/SARS-CoV-2-NC_045513.fa

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



