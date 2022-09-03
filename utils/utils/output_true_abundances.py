
import pandas as pd
import argparse
from collections import Counter
import sys


def main():
    parser = argparse.ArgumentParser(description="Given the metadata file of some benchmark and the voc simulated & its abundance, it calulates the true abundance for each lineage in the benchmark")
    parser.add_argument('--m', dest = 'metadata', required=True, type=str, help="relative path to metadata file")
    parser.add_argument('--voc', dest = 'voc', required=True, type=str, help="simulated voc/lineage")
    parser.add_argument('--voc_ab', dest = 'voc_ab', required=True, type=int, help="abundance simulated for the voc/lineage")
    parser.add_argument('--min_ab', dest = 'min_ab', required=True, type=float, help="minimum abundance threshold")
    parser.add_argument('--outdir', dest = 'outdir', required=True, type=str, help="directory to output resutls")
    args = parser.parse_args()

    # read metadata
    print("reading metadata...", flush=True)
    metadata_df = pd.read_csv(args.metadata, sep='\t', header=0, dtype=str)

    print("reading metadata: done", flush=True)

    total_amount_of_sequences = len(metadata_df["Pango lineage"])
    counts_per_lineage = Counter(metadata_df["Pango lineage"]).items()

    print("Amount of sequences per lineage: ", counts_per_lineage)
    print("Total amount of sequences: ", total_amount_of_sequences)

    total_ab = 100
    left_over_ab = total_ab - args.voc_ab

    true_ab_dict = dict()
    
    # initialize dict lineage - true abundance to zero
    for lineage in Counter(metadata_df["Pango lineage"]).keys():
        true_ab_dict[lineage] = dict()
        true_ab_dict[lineage]["true_ab"] = 0
        true_ab_dict[lineage]["adj_ab"] = 0

    # initialize voc abundance
    true_ab_dict[args.voc]["true_ab"] = args.voc_ab

    # calculate true abundances 

    for (lin, count) in counts_per_lineage:

        ab_per_sequence = left_over_ab/total_amount_of_sequences
        true_ab_dict[lin]["true_ab"] += ab_per_sequence * count

        true_ab_dict[lin]["true_ab"] = round(true_ab_dict[lin]["true_ab"], 2)
        true_ab_dict[lin]["adj_ab"] = round(true_ab_dict[lin]["true_ab"], 2)

        if true_ab_dict[lin]["true_ab"] < args.min_ab:
            true_ab_dict[lin]["adj_ab"] = 0
    
    # calculate adjusted abundances
    sum_of_adj = 0
    for (lin, count) in counts_per_lineage:

        sum_of_adj += true_ab_dict[lin]["adj_ab"] 
    
    print("Sum of  adjusted abundances", sum_of_adj )

    for (lin, count) in counts_per_lineage:
        true_ab_dict[lin]["adj_ab"]  =  true_ab_dict[lin]["adj_ab"]/sum_of_adj * 100
        true_ab_dict[lin]["adj_ab"] = round(true_ab_dict[lin]["adj_ab"], 2)
    
    sum_of_adj = 0
    for (lin, count) in counts_per_lineage:
        sum_of_adj += true_ab_dict[lin]["adj_ab"] 
    
    print("Sum of (corrected) adjusted abundances", sum_of_adj )

    res_dict = pd.DataFrame.from_dict(true_ab_dict)

    print(res_dict)

    print("writing results...")
    res_dict.to_csv(args.outdir + "/true_benchmark_abundances.tsv", sep="\t")
    print("done")

    return



if __name__ == "__main__":
    sys.exit(main())