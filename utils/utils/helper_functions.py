import os
import pandas as pd
import json
from Bio import SeqIO
import time

# Output predictions as json file for proximity experiments
def output_results_to_json(dir_name, threshold, ref_sets, seeds, abundances, seq_name):
    
    all_files = getListOfFiles(dir_name)
    lineage_measured = seq_name.split("_")[0]
    results = dict()

    for ref_set in ref_sets:
        results[ref_set] = dict()
        for seed in seeds:
            results[ref_set][seed] = dict()
            for ab in abundances:
                print(ref_set, seed, ab)
                path = "kallisto_predictions/{}/seed_{}/{}_ab{}/predictions_m{}.tsv".format(ref_set, seed, seq_name, ab, threshold)
                res_files = list(filter(lambda p: path in p, all_files))
                predictions_df = pd.read_csv(res_files[0],sep='\t',skiprows=3, header = None)

                for i in range(0, len(predictions_df)):
                    if predictions_df[0][i] == lineage_measured:
                        results[ref_set][seed][ab]= predictions_df[2][i]
                        break
                
                    if ab not in results[ref_set][seed].keys():
                        results[ref_set][seed][ab] = 0
        
    with open(dir_name + '/results.json', 'w') as f:
        json.dump(results, f)
    
    return 

# Output predictions as json file for allele frequency experiments
def output_results_to_json_3_dirs(first_dir, threshold, second_dirs, third_dirs, abundances, seq_name):
    
    all_files = getListOfFiles("kallisto_predictions/" + first_dir + "/")
    lineage_measured = seq_name.split("_")[0]
    results = dict()

    for second_dir in second_dirs:
        results[second_dir] = dict()
        for third_dir in third_dirs:
            results[second_dir][third_dir] = dict()
            for ab in abundances:
                path = "kallisto_predictions/{}/{}/{}/{}_ab{}/predictions_m{}.tsv".format(first_dir, second_dir, third_dir, seq_name, ab, threshold)
                res_files = list(filter(lambda p: path in p, all_files))
                predictions_df = pd.read_csv(res_files[0],sep='\t',skiprows=3, header = None)

                for i in range(0, len(predictions_df)):
                    if predictions_df[0][i] == lineage_measured:
                        results[second_dir][third_dir][ab]= predictions_df[2][i]
                        break
                
                    if ab not in results[second_dir][third_dir].keys():
                        results[second_dir][third_dir][ab] = 0
        
    with open('results_{}.json'.format(first_dir), 'w') as f:
        json.dump(results, f)
    
    return 


# For the given path, get the List of all files in the directory tree 
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

# calculate absolute errors for proximity experiments
def calculate_absolute_errors(results_dict, seeds, abundances, ref_sets):
    absolute_errors = dict()

    for ref_set in ref_sets:
        absolute_errors[ref_set] = dict()
        for ab in abundances:
            absolute_errors[ref_set][ab] = dict()
            for seed in seeds:
                absolute_errors[ref_set][ab][seed] = round(abs(ab - results_dict[ref_set][str(seed)][str(ab)]), 3)


    return absolute_errors
# calculate absolute errors for allele frequency optimization experiment
def calculate_absolute_errors_af(results_dict, allele_freqs, abundances, ref_sets_dict, continents):
    abs_errors = dict()

    for continent in continents: 
        abs_errors[continent] = dict()
        for ref_set in ref_sets_dict[continent]:
            abs_errors[continent][ref_set] = dict()
            for af in allele_freqs:
                af = str(af)
                abs_errors[continent][ref_set][af] = dict()
                for ab in abundances:
                    absolute_error = round(abs(ab - results_dict[continent][ref_set][af][str(ab)]), 3)
                    abs_errors[continent][ref_set][af][str(ab)] = absolute_error
    return abs_errors

# given a fasta file and a list of sequence identifiers,
# returns the sequences that are not included in the list of identifiers provided.
# a the fasta file with the resulting sequences are saved under
# the name of the target file provided as input.
def filter_fasta(fasta_file, identifiers, target_file):
    print(len(identifiers), " sequences to be removed")
    
    if os.path.exists(target_file):
        os.remove(target_file)
    
    seqs = []
    
    for seq in SeqIO.parse(fasta_file, "fasta"):
        if (identifiers.count(seq.description.strip()) == 0):
            seqs.append(seq) 
    
    print("Writing sequences: ", len(seqs))
    # Write sequences to file
    with open(target_file, "w") as target:
        SeqIO.write(seqs, target, "fasta")

    print("Done, results can be found in "  + target_file)

    f_ids = parse_fasta(target_file)
    print("Final number of sequences : ", len(f_ids))
    return


# returns sequence identifiers given a fasta file.
def parse_fasta(fname):
    identifiers = []
    with open(fname, "r") as fh:
        for line in fh:
            if line.startswith(">"):
                identifiers.append(line[1:].strip())
    return identifiers

def filter_dataset_by_date(metadata_inpt, fasta, outdir, start_date, end_date):
    # make directory
    if not os.path.isdir(outdir) :
        os.mkdir(outdir)
    
    # define target files
    target_mt = os.path.join(os.curdir, outdir, "metadata.tsv")
    target_fasta = os.path.join(os.curdir, outdir, "sequences.fasta")

    # delete target files if they exist
    if os.path.exists(target_mt):
        os.remove(target_mt)

    if os.path.exists(target_fasta):
        os.remove(target_fasta)
    
    # create target files (metadata) fasta is being created by the function filter_fasta
    metadata = open(target_mt, "x")
    metadata = open(target_mt, "a")

    # read metadata 
    metadata_df = pd.read_csv(metadata_inpt, sep='\t', dtype=str)
    initial_identifiers = metadata_df['strain']
    # filter metadata based on date
    metadata_df = metadata_df[(metadata_df['date'] >= start_date) & (metadata_df['date'] <= end_date)]
    to_be_kept_identifiers = metadata_df['strain']

    to_be_removed_identifiers = list(initial_identifiers[~initial_identifiers.isin(to_be_kept_identifiers)])

    # write_metadata
    metadata_df.to_csv(target_mt, sep='\t')
    # Select and write corresponding fasta
    filter_fasta(fasta, to_be_removed_identifiers, target_fasta)


    return 

def output_dataset_info(lineage, metadata_dir, selection_metadata_dir):
    data_info = dict()
    if selection_metadata_dir != None:
        select_mt_file = pd.read_csv(selection_metadata_dir + "/metadata.tsv", sep='\t')
    # find max and min date from metadata
        selection_amount_of_seqs = len(select_mt_file)
        selection_amount_of_lineage_measured_seqs = select_mt_file["pango_lineage"].value_counts()[lineage]
        data_info["Amount of {} sequences (after selection)".format(lineage)] = selection_amount_of_lineage_measured_seqs 
        data_info["Total amount of sequences (after selection)"] =  selection_amount_of_seqs
        pass

    # load tsv file 
    mt_file = pd.read_csv(metadata_dir + "/metadata.tsv", sep='\t')
    # find max and min date from metadata
    max_date = mt_file['date'].max()
    min_date = mt_file['date'].min()
    amount_of_seqs = len(mt_file)
    amount_of_lineage_measured_seqs = mt_file["pango_lineage"].value_counts()[lineage]
    amount_of_unique_lineages =mt_file['pango_lineage'].nunique()

    # Write data info to dictionary
    data_info["Timespan"] = "{} till {}".format(max_date, min_date)
    data_info["Total amount of sequences"] =  amount_of_seqs
    data_info["Amount of {} sequences".format(lineage)] = amount_of_lineage_measured_seqs
    data_info["Amount of lineages"] = amount_of_unique_lineages

    data_info = pd.DataFrame.from_dict([data_info])
    data_info.to_csv(metadata_dir + "/dataset_info.csv")

    return 