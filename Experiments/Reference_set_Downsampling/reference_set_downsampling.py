import sys
import os
import argparse
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from utils.helper_functions import filter_fasta

def main():
    parser = argparse.ArgumentParser(description="Downsample reference set")
    parser.add_argument('--m', dest = 'metadata', required=True, type=str, help="metadata filee of sequences to be downsampled")
    parser.add_argument('--f', dest = 'fasta', required=True, type=str, help="fasta file of sequences to be downsampled")
    parser.add_argument('--seed', dest = 'seed', required=True, type=int, help="random seed")
    parser.add_argument('--ref_set', dest = 'ref_set', required=True, type=str, help="reference set")
    parser.add_argument('--frac', dest = "frac", required=False, type=float, default=0.10, help="fraction of sequences ot be deleted")

    args = parser.parse_args()

    metadata_df = pd.read_csv(args.metadata, sep='\t', header=0, dtype=str)
    
    pango_lin = 'pangolin_lineage'

    if pango_lin not in metadata_df:
        pango_lin = "pango_lineage"

    lineages_to_del  = metadata_df.sample(frac=args.frac, random_state=args.seed)
    lineages_to_del_id = lineages_to_del["strain"].tolist()

    

    # filter and write fasta
    filter_fasta(Path(args.fasta).absolute(), lineages_to_del_id, os.path.join(os.path.curdir , args.ref_set,("sequences_filtered_" + str(args.seed)+".fasta")))
    boolean_series = ~metadata_df.strain.isin(lineages_to_del_id)

    # filter metadata
    filtered_metadata = metadata_df[boolean_series]

    print("Inital number of sequences ", len(metadata_df))

    print("metadata is ready! ", len(filtered_metadata), " sequences written")
    # write metadata
    filtered_metadata.to_csv(os.path.join(os.curdir,  args.ref_set, ("metadata_filtered_" + str(args.seed) + ".tsv")), sep='\t')
    
    return

if __name__ == "__main__":
    sys.exit(main()) 


