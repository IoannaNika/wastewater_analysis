#!/bin/sh

mkdir -p reference_sets
# initial dataset downloaded from GISAID on 2022-06-12
end_date="2022-01-01"

metadata="../../../../../GISAID/gisaid_2022_06_12/metadata.tsv"
sequences="../../../../../GISAID/gisaid_2022_06_12/sequences.fasta"

for location_info in "Connecticut,state,Connecticut" "USA,country,USA" "North America,continent,North_America" "Global,all,Global"; do \
    IFS=','
    set -- $location_info
    location=$1
    location_type=$2
    folder_name=$3
    outdir=reference_sets/$folder_name
    mkdir -p $outdir

    for start_date in "2020-01-01" "2020-06-01" "2021-01-01" "2021-06-01"; do \

        outdir=reference_sets/$folder_name/${start_date}_till_${end_date}
        mkdir -p $outdir

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
    done
done 
        

