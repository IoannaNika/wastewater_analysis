import os
import pandas as pd
import sys
import argparse
import itertools


from helper_functions import filter_fasta



def main():
    parser = argparse.ArgumentParser(description="Filters dataset absed on date")
    parser.add_argument('--m', dest = 'metadata', required=True, type=str, help="relative path to metadata file")
    parser.add_argument('--f', dest = 'fasta', required=True, type=str, help="relative path to fasta file")
    parser.add_argument('--dir_name', dest = 'dir_name', required=True, type=str, help="directory of dataset to be created")
    parser.add_argument('--start_date', dest = 'start_date', required=False, type=str, help="end date format (year-month-day)")
    parser.add_argument('--end_date', dest = 'end_date', required=False, type=str, help="start date format (year-month-day)")
    parser.add_argument('--continent', dest = "continent", required=False, type=str, help = "continent where the sequence was found")
    parser.add_argument('--country', dest = "country", required=False, type=str, help = "country where the sequence was found")
    parser.add_argument('--state', dest = "state", required=False, type=str, help = "state where the sequence was found")
    parser.add_argument('--ws', dest="write_seqs", required=True, type=bool,  help = "False for not writing sequences, True for writing sequences along with selected metadata" )
    args = parser.parse_args()

    # make directory
    if not os.path.isdir(args.dir_name) :
        os.mkdir(args.dir_name)

    # define target files
    target_mt = os.path.join(args.dir_name, "metadata.tsv")
    print("target file for metadata: ", target_mt, flush=True)
    target_fasta = os.path.join(args.dir_name, "sequences.fasta")
    print("target file for fasta: ", target_fasta , flush=True)

    # delete target files if they exist
    if os.path.exists(target_mt):
        os.remove(target_mt)

    if os.path.exists(target_fasta):
        os.remove(target_fasta)

    print("creating target files...", flush=True)
    # create target files (metadata) fasta is being created by the function filter_fasta
    open(target_mt, "x")
    open(target_mt, "a")

    print("reading metadata...", flush=True)
    # read metadata 
    metadata_df = pd.read_csv(args.metadata, sep='\t', header=0, dtype=str)

    print("reading metadata: done", flush=True)

    try:
        initial_identifiers = metadata_df['Virus name']
    except:
        initial_identifiers = metadata_df['strain']


    final_mt_df = metadata_df
    to_be_removed_ids_all = [] 

    # filter metadata based on start date
    if args.start_date:
        print("filter on start date", flush=True)
        try:
            keep_mt = metadata_df.loc[(metadata_df['Collection date'] >=  args.start_date)]
        except:
            keep_mt = metadata_df.loc[(metadata_df['date'] >=  args.start_date)]
        try:
            to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))
        except:
            to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["strain"])]))

        print("start date considered for metadata", flush=True)

    # filter metadata based on end date
    if args.end_date:
        print("filter on end date", flush=True)
        try:
            keep_mt = metadata_df.loc[(metadata_df['Collection date'] <= args.end_date)]
        except:
            keep_mt = metadata_df.loc[(metadata_df['date'] <= args.end_date)]
        try:
            to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))
        except:
            to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["strain"])]))
        print("end date considered for metadata", flush=True)
    # filter by location
    if args.state: 
        print("filter on location: state", flush=True)
        keep_mt = metadata_df.loc[metadata_df['Location'].str.endswith("/ " + args.state)]
        try:
            to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))
        except:
            to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["strain"])]))
        print("state considered for metadata", flush=True)
    if args.country:
        print("filter on location: country", flush=True)
        keep_mt = metadata_df.loc[metadata_df['Location'].str.contains(" / " + args.country + " / ")]
        try:
            to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))
        except:
             to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["strain"])]))
        print("country considered for metadata", flush=True)
    if args.continent:
        print("filter on location: continent", flush=True)
        keep_mt = metadata_df.loc[metadata_df['Location'].str.startswith(args.continent)]
        try:
            to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))
        except:
            to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["strain"])]))
        print("continent considered for metadata", flush=True)

    print("writing metadata...", flush=True)
    to_be_removed_ids_all= list(itertools.chain.from_iterable(to_be_removed_ids_all))
    try:
        final_mt_df = final_mt_df[~final_mt_df["Virus name"].isin(to_be_removed_ids_all)]
    except:
        final_mt_df = final_mt_df[~final_mt_df["strain"].isin(to_be_removed_ids_all)]
    # write_metadata
    final_mt_df.to_csv(target_mt, sep='\t')
    # Select and write corresponding fasta
    print("metadata have been written", flush=True)
    
    if args.write_seqs == True:
        print("writing sequences...", flush=True)
        filter_fasta(args.fasta, list(set(to_be_removed_ids_all)), target_fasta)
        print("write sequences done", flush=True)
    return

if __name__ == "__main__":
    sys.exit(main())



    