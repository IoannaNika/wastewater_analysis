import os
import pandas as pd
import sys
import argparse
import itertools


from utils.helper_functions import filter_fasta



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

    args = parser.parse_args()

    # make directory
    if not os.path.isdir(args.dir_name) :
        os.mkdir(args.dir_name)

    # define target files
    target_mt = os.path.join(args.dir_name, "metadata.tsv")
    target_fasta = os.path.join(args.dir_name, "sequences.fasta")

    # delete target files if they exist
    if os.path.exists(target_mt):
        os.remove(target_mt)

    if os.path.exists(target_fasta):
        os.remove(target_fasta)
    
    # create target files (metadata) fasta is being created by the function filter_fasta
    open(target_mt, "x")
    open(target_mt, "a")

    # read metadata 
    metadata_df = pd.read_csv(args.metadata, sep='\t', header=0, dtype=str)
    initial_identifiers = metadata_df['Virus name']


    final_mt_df = metadata_df
    to_be_removed_ids_all = [] 

    # filter metadata based on start date
    if args.start_date:
        keep_mt = metadata_df[(metadata_df['date'] >=  args.start_date)]
        to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))

    # filter metadata based on end date
    if args.end_date:
        keep_mt = metadata_df[(metadata_df['date'] <= args.end_date)]
        to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))

    # filter by location
    if args.state: 
        keep_mt = list(metadata_df[metadata_df['Location'].str.endswith("/ " + args.state)])
        to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))

    if args.country:
        keep_mt = metadata_df[metadata_df['Location'].str.contains(" / " + args.country + " / ")]
        to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))
        
    if args.continent:
        keep_mt = metadata_df[metadata_df['Location'].str.startswith(args.continent)]
        to_be_removed_ids_all.append(list(initial_identifiers[~initial_identifiers.isin(keep_mt["Virus name"])]))

    to_be_removed_ids_all= list(itertools.chain.from_iterable(to_be_removed_ids_all))
    final_mt_df = final_mt_df[~final_mt_df["Virus name"].isin(to_be_removed_ids_all)]
    # write_metadata
    final_mt_df.to_csv(target_mt, sep='\t')
    # Select and write corresponding fasta

    
    filter_fasta(args.fasta, list(set(to_be_removed_ids_all)), target_fasta)

    return

if __name__ == "__main__":
    sys.exit(main())



    