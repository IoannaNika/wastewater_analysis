
import pandas as pd
import argparse
from collections import Counter
import sys


def main():
    parser = argparse.ArgumentParser(description="Given the metadata file of some benchmark and the voc simulated & its abundance, it calulates the true abundance for each lineage in the benchmark")
    parser.add_argument('--m', dest = 'metadata', required=True, type=str, help="relative path to metadata file")
    parser.add_argument('--voc', dest = 'voc', required=True, type=str, help="simulated voc/lineage")
    parser.add_argument('--voc_ab', dest = 'voc_ab', required=True, type=float, help="abundance simulated for the voc/lineage")
    parser.add_argument('--min_ab', dest = 'min_ab', required=True, type=float, help="minimum abundance threshold")
    parser.add_argument('--ref_set_locations', dest = 'locations', required=False, type=str, help="comma seperated string with reference set locations")
    parser.add_argument('--ref_set_dir', dest = 'ref_set_dir', required=False, type=str, help="path to reference sets")
    parser.add_argument('--outdir', dest ='outdir', required=True, type=str, help="directory to output resutls")
    args = parser.parse_args()

    # read metadata
    print("reading metadata...", flush=True)
    metadata_df = pd.read_csv(args.metadata, sep='\t', header=0, dtype=str)

    print("reading metadata: done", flush=True)

    total_amount_of_sequences = len(metadata_df["Pango lineage"])
    counts_per_lineage = Counter(metadata_df["Pango lineage"]).items()

    # print("Amount of sequences per lineage: ", counts_per_lineage)
    # print("Total amount of sequences: ", total_amount_of_sequences)

    total_ab = 100
    left_over_ab = total_ab - args.voc_ab

    true_ab_dict = dict()
    
    # initialize dict lineage - true abundance to zero
    for lineage in Counter(metadata_df["Pango lineage"]).keys():
        true_ab_dict[lineage] = dict()
        true_ab_dict[lineage]["true_ab"] = 0
        true_ab_dict[lineage]["adj_ab"] = 0

    # initialize voc abundance
    try:
        true_ab_dict[args.voc]["true_ab"] = args.voc_ab
    except:
        pass

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
    
    # print("Sum of  adjusted abundances", sum_of_adj )

    for (lin, count) in counts_per_lineage:
        true_ab_dict[lin]["adj_ab"]  =  true_ab_dict[lin]["adj_ab"]/sum_of_adj * 100
        true_ab_dict[lin]["adj_ab"] = round(true_ab_dict[lin]["adj_ab"], 2)
    
    sum_of_adj = 0
    for (lin, count) in counts_per_lineage:
        sum_of_adj += true_ab_dict[lin]["adj_ab"] 
    
    # print("Sum of (corrected) adjusted abundances", sum_of_adj )

    print("find predictions per lineage...")

    if args.locations:
        locs =  args.locations.split(",")
        for loc in locs:
            # read abundance predictions
            predictions_path = "Experiments/Sub_lineages_Experiments/Omicron/kallisto_predictions_test/{}/_ab12.5/predictions_m0.1.tsv".format(loc)
            predictions_df = pd.read_csv(predictions_path, sep='\t',skiprows=3, header = None)
            
            for (lin, count) in counts_per_lineage:
                for i in range(0, len(predictions_df)):
                    if predictions_df[0][i] == lin:
                        true_ab_dict[lin]["predictions_{}".format(loc)] = predictions_df[3][i]

                if "predictions_{}".format(loc) not in true_ab_dict[lin].keys():
                    true_ab_dict[lin]["predictions_{}".format(loc)] = 0

                true_ab_dict[lin]["absolute_error_{}".format(loc)] = round(abs(true_ab_dict[lin]["adj_ab"]- true_ab_dict[lin]["predictions_{}".format(loc)]),2)


    print("find amount of reference sequences per lineage in benchmark in the given reference sets....")

    if args.locations and args.ref_set_dir:
        locs =  args.locations.split(",")
        for loc in locs:
            path = args.ref_set_dir + loc
            # read metadata
            metadata_df = pd.read_csv(path + "/metadata.tsv", sep='\t', header=0, dtype=str)
            lin_counts = Counter(metadata_df["Pango lineage"])

            for (lin, count) in counts_per_lineage:
                try:
                    true_ab_dict[lin][loc + "_amount_of_ref_sequences"] = lin_counts[lin]
                except:
                    true_ab_dict[lin][loc + "_amount_of_ref_sequences"] = 0

    res_dict = pd.DataFrame.from_dict(true_ab_dict)

    print(res_dict)

    print("writing results...")
    res_dict.to_csv(args.outdir + "/true_benchmark_abundances.tsv", sep="\t")
    print("done")


    return



if __name__ == "__main__":
    sys.exit(main())