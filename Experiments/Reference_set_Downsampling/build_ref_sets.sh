
for  seed in 1 2 3 4 5 6 7 8 9 10; do \
  for ref_set in "Netherlands" "Netherlands_nearby_countries" "Europe" "Global_next_regions"; do \
        python ../../manuscript/preprocess_references_v1.py -m  reference_sets/${ref_set}/metadata_filtered_${seed}.tsv -f reference_sets/${ref_set}/sequences_filtered_${seed}.fasta --seed 0 -o  reference_sets/${ref_set}/reference_set_${seed}
        bash ../../pipeline/pipeline/call_variants.sh reference_sets/${ref_set}/reference_set_${seed} /Users/ioanna/Projects/CSE3000_wastewater_project/data/SARS-CoV-2-NC_045513.fasta
        python ../../manuscript/select_samples_v1.py -m reference_sets/${ref_set}/metadata_filtered_${seed}.tsv -f reference_sets/${ref_set}/sequences_filtered_${seed}.fasta -o reference_sets/${ref_set}/reference_set_${seed} --vcf reference_sets/${ref_set}/reference_set_${seed}/*_merged.vcf.gz --freq reference_sets/${ref_set}/reference_set_${seed}/*_merged.frq
        kallisto index -i reference_sets/${ref_set}/reference_set_${seed}/sequences.kallisto_idx reference_sets/${ref_set}/reference_set_${seed}/sequences.fasta
    
    # remove everything except the metadata file, the fasta file, the lineage contents file & the kallisto index

        for file in reference_sets/${ref_set}/reference_set_${seed}/*; do \

            if [ -d "$file" ] ; then
                echo "$file is a directory and it will be removed";
                rm -r $file
            fi

            if ! [[ "$file"  =~ ^(reference_sets/${ref_set}/reference_set_${seed}/metadata.tsv|reference_sets/${ref_set}/reference_set_${seed}/sequences.kallisto_idx|reference_sets/${ref_set}/reference_set_${seed}/sequences.fasta|reference_sets/${ref_set}/reference_set_${seed}/lineages.txt)$ ]]; 
            then 
                echo "$file is removed"
                rm $file
            fi
        done
    done
done

