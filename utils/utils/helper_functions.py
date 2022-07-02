import os
from posixpath import dirname
from numpy import absolute
import pandas as pd
import json
from Bio import SeqIO

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

def calculate_absolute_errors(results_dict, seeds, abundances, ref_sets):
    absolute_errors = dict()

    for ref_set in ref_sets:
        absolute_errors[ref_set] = dict()
        for ab in abundances:
            absolute_errors[ref_set][ab] = dict()
            for seed in seeds:
                absolute_errors[ref_set][ab][seed] = round(abs(ab - results_dict[ref_set][str(seed)][str(ab)]), 3)


    return absolute_errors

# given a fasta file and a list of sequence identifiers,
# returns the sequences that are not included in the list of identifiers provided.
# a the fasta file with the resulting sequences are saved under
# the name of the target file provided as input.
def filter_fasta(fasta_file, identifiers, target_file):
    print(len(identifiers))
    
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
