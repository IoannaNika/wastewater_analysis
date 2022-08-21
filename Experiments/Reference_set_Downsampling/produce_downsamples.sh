mkdir reference_sets
for seed in 1 2 3 4 5 6 7 8 9 10; do \
    for ref_set in "Netherlands ../../data/Proximity_Experiments/Europe/reference_sets/Netherlands" \
    "Netherlands_nearby_countries ../../data/Proximity_Experiments/Europe/reference_sets/Netherlands_nearby_countries" \
    "Europe ../../data/Proximity_Experiments/Europe/reference_sets/Europe" \
    "Global_next_regions ../../data/Proximity_Experiments/Europe/reference_sets/Global_next_regions" ; do \
        set -- $ref_set 
        mkdir reference_sets/$1
        python reference_set_downsampling.py --ref_set reference_sets/$1 --m $2/metadata.tsv --f $2/sequences.fasta --seed ${seed}

    done
done