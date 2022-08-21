mkdir -p reference_sets

metadata="../../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
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

    if [[ "$location_type" == "all" ]] ; then
        # preprocess references
        python ../../../utils/utils/filter_dataset.py --m $metadata --f $sequences --start_date $start_date --end_date $end_date --dir_name $outdir
    elif [[ "$location_type" == "continent" ]] ; then
        # preprocess references
        python ../../../utils/utils/filter_dataset.py --m $metadata --f $sequences --continent $location --start_date $start_date --end_date $end_date --dir_name $outdir
    
    elif [[ "$location_type" == "country" ]] ; then
        # preprocess references
        python ../../../utils/utils/filter_dataset.py --m $metadata --f $sequences --country $location --start_date $start_date --end_date $end_date --dir_name $outdir

    else [[ "$location_type" == "state" ]]
        # preprocess references
        python ../../../utils/utils/filter_dataset.py --m $metadata --f $sequences --state $location --start_date $start_date --end_date $end_date --dir_name $outdir

    fi
    # Now in reference_sets/... there is a metadata.tsv file with metadata for sequences that fall into the specified locations & dates
    
    # Produce downsamples
    for seed in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do \
        python ../../../utils/utils/reference_set_downsampling.py --ref_set $outdir --m $outdir/metadata.tsv --seed ${seed}
    done
done
