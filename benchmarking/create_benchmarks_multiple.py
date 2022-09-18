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
    parser.add_argument('-fv, --fasta_voc', dest='fasta_VOC', required=True, type=str,
                        help="comma-separated list of fasta files for Variants Of Concern (VOC)")
    parser.add_argument('-o, --outdir', dest='outdir', required=True, type=str,
                        help="output directory")
    parser.add_argument('--voc_perc', dest='voc_perc', required=True, type=str,
                        help="comma-separated list of VOC frequencies (%) to be simulated")
    parser.add_argument('--total_cov', dest='total_cov', default=10000, type=int,
                        help="total sequencing depth to be simulated")
    parser.add_argument('--data_exploration_only', action='store_true',
                        help="exit after sequence selection")
    parser.add_argument('--spike_only', action='store_true',
                        help="simulate reads for spike region only")
    parser.add_argument('--seed', dest='seed', default=42, type=int)
    parser.add_argument('--div', dest='div', default=None, type=int, help="amount of sequences to be simulated as VOC")

    args = parser.parse_args()
    # create output directory
    try:
        os.mkdir(args.outdir)
    except FileExistsError:
        pass

    VOC_frequencies = args.voc_perc.split(',')
    total_cov = args.total_cov
    VOC_files = args.fasta_VOC.split(',')
    seed = args.seed
    VOC_names = [filepath.split('/')[-1] for filepath in VOC_files]
    print("VOC_names:")
    print(VOC_names)
    # excluding genome sequences that we are simulating from the background so that the composition
    # is not messed up.
    exclude_list = [name.split('_')[0] for name in VOC_names]
    print("Exclude list")
    print(exclude_list)
    # Read metadata from tsv into dataframe
    full_df = read_metadata(args.metadata)
    # print('METADATA FILE')
    # print(full_df)
    # Filter metadata file(later we will filter corresponding fasta)
    selection_df = select_benchmark_genomes(full_df, args.state, args.date,
                                            exclude_list)
    # filter fasta according to selection and write new fasta
    fasta_selection = args.outdir + "/sequences.fasta"
    # Generates the sequences.fasta file
    #         GISAID/half.fasta,   path to sequences.fasta, filtered dataframe of metadata file
    # New sequences.fasta file that is generated contains only the filtered sequences
    # from original fasta file. This is the sequence file that will be used to simulate ww sequencing reads.
    filter_fasta(args.fasta_ref, fasta_selection, selection_df)
    print("Selected sequences written to {}".format(fasta_selection))
    # write corresponding metadata to tsv
    metadata_out = args.outdir + "/metadata.tsv"
    print("Selection df")
    print(selection_df)
    selection_df.to_csv(metadata_out, sep='\t', index=False)
    print("Metadata for selected sequences is in {}".format(metadata_out))

    # Till now we  have only filtered the metadata and
    # fasta file according to the requirements/constraints put in
    # the benchmark command, these sequences will be used as background sequences in the wastewater files
    # and art illumina will simulate what is read from wastewater which contains these sequences as backgound \
    # + the actual simulated genomes
    if args.data_exploration_only:
        sys.exit()

    if args.spike_only:
        # trim sequences to select spike region
        print("\nTrimming genomes around spike region (21063--25884)")
        trimmed_selection = args.outdir + "/sequences.trimmed.fasta"
        subprocess.check_call(
            "reformat.sh in={} out={} fastawrap=0 overwrite=t forcetrimleft=21063 forcetrimright=25884".format(
                fasta_selection, trimmed_selection), shell=True)
        # also trim VOC sequences
        for filename in VOC_files:
            VOC_name = filename.rstrip('.fasta').split('/')[-1]
            trimmed_file = args.outdir + "/{}.trimmed.fasta".format(VOC_name)
            subprocess.check_call(
                "reformat.sh in={} out={} fastawrap=0 overwrite=t forcetrimleft=21063 forcetrimright=25884".format(
                    filename, trimmed_file), shell=True)
        fasta_selection = trimmed_selection
        print("\nSpike sequences ready\n")

    # simulate reads at specific frequencies
    for VOC_freq in VOC_frequencies:
        # simulate reads for background sequences
        VOC_cov = total_cov * float(VOC_freq) / 100
        # Round of 2 decimal point so 1.99 becomes 2.00
        VOC_cov = round(VOC_cov, 2)
        # length of selection df =# of background sequences
        # basically backgound_cov is the freq of every single background seq in selection_df I think?
        # Example if voc_cov is 50 and #selection df seqs=10 then every seq in
        # background will be a selection df seq at 50/10=5% abundance and
        # 10 such seqs =50% of the total sample being background seqs.
        background_cov = round((total_cov - VOC_cov) / len(selection_df.index), 2)
        print("Simulating reads from {} at {}x coverage".format(fasta_selection,
                                                                background_cov))
        # fasta_selection is the filtered new sequences file
        # containing only the list of background sequences
        subprocess.check_call(
            # Simulate background files, here input is full sequences file that comprise
            # all background sequences
            "art_illumina -ss HS25 --rndSeed {3} -i {0} -l 150 -f {1} -p -o {2}/background_{1}x -m 250 -s 10"
            .format(fasta_selection, background_cov, args.outdir, seed), shell=True)
        # print("Making combined file")
        # Make empty file which will contain combined genome sim files
        file1 = args.outdir+"/" + "/combined_" + str(VOC_cov) + "x1.fq"
        file2 = args.outdir+"/" + "/combined_" + str(VOC_cov) + "x2.fq"

        open(file1, 'a').close()
        open(file2, 'a').close()

        # subprocess.check_call("cat > {0}/combined_{1}x1.fq".format(args.outdir, VOC_cov), shell=True)
        # subprocess.check_call("cat > {0}/combined_{1}x2.fq".format(args.outdir, VOC_cov), shell=True)

        # simulate reads for VOC, then merge and shuffle
        for filename in VOC_files:
            # print("Started inner loop")
            # Example VOC_name="B.1.621.1_EPI_ISL_4366266"
            VOC_name = filename.rstrip('.fasta').split('/')[-1]

            if args.spike_only:
                voc_fasta = args.outdir + "/{}.trimmed.fasta".format(VOC_name)
            else:
                print("EXAMPLE VOC Name:", VOC_name)
                voc_fasta = filename
            print("Simulating reads from {} at {}x coverage".format(VOC_name,
                                                                    VOC_cov))
            div  = args.div
            print("Making file:{2}/{3}_{1}x".format(voc_fasta, VOC_cov/div, args.outdir, VOC_name))
            subprocess.check_call(
                "art_illumina -ss HS25 --rndSeed {4} -i {0} -l 150 -f {1} -p -o {2}/{3}_{1}x -m 250 -s 10".format(voc_fasta, VOC_cov/div, args.outdir, VOC_name, seed), shell=True)
            # Add this file to combined sim file containing all genome files
            # Combine x1 with x1 file
            print("Trying to access file:{0}/{2}_{3}x1.fq ".format(args.outdir, background_cov, VOC_name, VOC_cov/div))

            try:
                subprocess.check_call(
                    "cat {0}/combined_{3}x1.fq {0}/{2}_{3}x1.fq > {0}/combined_{3}x1.fq".format(args.outdir, background_cov, VOC_name, VOC_cov/div), shell=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            # Combine x2 with x2 file
            subprocess.check_call(
                "cat {0}/combined_{3}x2.fq {0}/{2}_{3}x2.fq > {0}/combined_{3}x2.fq".format(args.outdir, background_cov, VOC_name, VOC_cov/div), shell=True)
            # print("Finished inner loop once")
        # Combine background with file containing all fq files
        # tmp1.fq contains both background and gen seqs simulated at abundance VOC_freq for the forward step
        # For x1
        subprocess.check_call("cat {0}/background_{1}x1.fq {0}/combined_{2}x1.fq > {0}/tmp1.fq".
                              format(args.outdir, background_cov, VOC_cov/div), shell=True)
        # For x2
        subprocess.check_call("cat {0}/background_{1}x2.fq {0}/combined_{2}x2.fq > {0}/tmp2.fq".
                              format(args.outdir, background_cov, VOC_cov/div), shell=True)
        print("\nMerging fastqs...")
        # For combined lineages in same ww sim file you need to concatenate
        # all x1 files with each other and all x2 files with each other
        # background file is for specific abundances and are not connected to specific lineages/genomes you have
        # 33 abundances * 2(forward/reverse step) * 2 lineages I think for mu=132 background files.
        print("Shuffling reads...")
        # The shuffle script is included in bbmap
        subprocess.check_call(
            "shuffle.sh in={0}/tmp1.fq in2={0}/tmp2.fq out={0}/wwsim_{1}_ab{2}_1.fastq "
            "out2={0}/wwsim_{1}_ab{2}_2.fastq overwrite=t fastawrap=0".format(
                args.outdir, VOC_name, VOC_freq), shell=True)
        print("\nBenchmarks with a VOC frequency of {}% are ready!\n\n".format(VOC_freq))
    # clean up temporary files
    os.remove("{}/tmp1.fq".format(args.outdir))
    os.remove("{}/tmp2.fq".format(args.outdir))
    return


# Filter the dataframe to select only rows from state,date and exlude all in exclude list.
def select_benchmark_genomes(df, state, date, exclude_list):
    """Select genomes by location and date"""
    selection_df = df
    # loc is for extracting values at specific location-row or column in a df
    # state_df = df.loc[df["division"] == state]
    # selection_df = state_df.loc[state_df["date"] == date]
    # For each distinct pango lineages print how many
    # times it is found in the file according to state and date filtered.
    print("\nLineage counts for {} on {}:".format(state, date))
    # Pango lineage refers to the name the particular virus lineage was given but the pango nomenclature
    print(selection_df["Pango lineage"].value_counts())
    print("\nExcluding VOC lineages {} from selection\n".format(exclude_list))
    # ~selection_df
    selection_df = selection_df.loc[
        ~selection_df["Pango lineage"].isin(exclude_list)]
    # # show number of samples per date
    # samples_per_date = state_df["date"].value_counts().sort_index()
    # print("Samples per date:")
    # with pd.option_context('display.max_rows', None,
    # 'display.max_columns', None):  # more options can be specified also
    #     print(samples_per_date)

    # # show lineages per date
    # grouped_mass_df = state_df.groupby(["date"])
    # print(grouped_mass_df.get_group(date)["strain", "pangolin_lineage"])
    # for key, item in grouped_mass_df:
    #     print(key, grouped_mass_df.get_group(key), "\n\n")
    return selection_df


if __name__ == "__main__":
    sys.exit(main())
