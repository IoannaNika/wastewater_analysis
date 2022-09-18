#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess
import pandas as pd
from random import randint
from select_samples import filter_fasta, read_metadata


def main():
    parser = argparse.ArgumentParser(description="Create wastewater benchmarks.")
    parser.add_argument('-m, --metadata', dest='metadata', type=str, help="metadata "
                                                                          "tsv file for full sequence database")
    parser.add_argument('-s, --state', dest='state', type=str, default="North America / USA / Connecticut",
                        help="sample location")
    parser.add_argument('-d, --date', dest='date', type=str, default="2021-04-30", help="sample date")

    # GISAID/half.fasta
    parser.add_argument('-fr, --fasta_ref', dest='fasta_ref', required=True,
                        type=str, help="fasta file representing full sequence database")
    parser.add_argument('-o, --outdir', dest='outdir', required=True, type=str,
                        help="output directory")
    parser.add_argument('--total_cov', dest='total_cov', default=10000, type=int,
                        help="total sequencing depth to be simulated")
    parser.add_argument('--data_exploration_only', action='store_true',
                        help="exit after sequence selection")
    parser.add_argument('--spike_only', action='store_true',
                        help="simulate reads for spike region only")
    parser.add_argument('--seed', dest='seed', default=42, type=int)

    args = parser.parse_args()

    # create output directory
    try:
        os.mkdir(args.outdir)
    except FileExistsError:
        pass

    # cleanup directory
    for root, dirs, files in os.walk(args.outdir):
        for f in files:
            os.remove( args.outdir + "/"+ f)

    total_cov = args.total_cov
    # VOC_files = args.fasta_VOC.split(',')
    seed = args.seed

    # Read metadata from tsv into dataframe
    full_df = read_metadata(args.metadata)

    # assume filtered beforeand
    selection_df = full_df
    # filter fasta according to selection and write new fasta
    fasta_selection = args.outdir + "/sequences.fasta"

    filter_fasta(args.fasta_ref, fasta_selection, selection_df)

    print("Selected sequences written to {}".format(fasta_selection))
    # write corresponding metadata to tsv
    metadata_out = args.outdir + "/metadata.tsv"
    selection_df.to_csv(metadata_out, sep='\t', index=False)
    print("Metadata for selected sequences is in {}".format(metadata_out))
    lin_list = list(set(selection_df["Pango lineage"]))

    ##############################################################################
    # calculate coverage per lineage
    total_amount_of_lin = len(lin_list)
    freq_per_lineage = 100/total_amount_of_lin
    cov_per_lineage = round(total_cov * float(freq_per_lineage)/100,2)
    print("Coverage per lineage", cov_per_lineage, total_amount_of_lin)
    print(lin_list)

    for lin in lin_list:
        total_amount_of_lin = len(lin_list)
        #amount of sequences per lineage
        seqs_per_lin = len(selection_df[selection_df["Pango lineage"] == lin])
        print("lineage:", lin,"sequences per lineage", seqs_per_lin)
        # write fasta
        metadata_for_lineage = selection_df[selection_df["Pango lineage"] == lin]
        fasta_selection_for_lineage = args.outdir + "/sequences_{}.fasta".format(lin)
        filter_fasta(args.fasta_ref, fasta_selection_for_lineage, metadata_for_lineage)
        
        subprocess.check_call("art_illumina -ss HS25 --rndSeed {4} -i {0} -l 150 -f {1} -p -o {2}/{3}_{1}x -m 250 -s 10".format(fasta_selection_for_lineage, (cov_per_lineage/seqs_per_lin), args.outdir, lin, seed), shell=True)
        
        # merge files
        subprocess.check_call("cat {0}/{1}_{2}x1.fq >> {0}/tmp1.fq".format(args.outdir, lin, cov_per_lineage/seqs_per_lin), shell=True)
        subprocess.check_call("cat {0}/{1}_{2}x2.fq >> {0}/tmp2.fq".format(args.outdir, lin, cov_per_lineage/seqs_per_lin), shell=True)
       
        subprocess.check_call("shuffle.sh in={0}/tmp1.fq in2={0}/tmp2.fq out={0}/wwsim_ab{1}_1.fastq out2={0}/wwsim_ab{1}_2.fastq overwrite=t fastawrap=0".format(args.outdir, cov_per_lineage), shell=True)
    return


if __name__ == "__main__":
    sys.exit(main())
