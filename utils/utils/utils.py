import os
from posixpath import dirname
import pandas as pd
import json

# Output predictions as json file for proximity experiments
def output_results_to_json(dir_name, threshold, continent, seeds, abundances, seq_name):
    all_files = getListOfFiles(dir_name)
    lineage_measured = seq_name.split("_")[0]
    results = dict()

    for seed in seeds:
        results[seed] = dict()
        for ab in abundances:
            path = "kallisto_predictions/{}}/seed_{}/{}_ab{}/predictions_m{}.tsv".format(continent, seed, seq_name, ab, threshold)
            res_files = list(filter(lambda p: path in p, all_files))
            predictions_df = pd.read_csv(res_files[0],sep='\t',skiprows=3, header = None)

            for i in range(0, len(predictions_df)):
                if predictions_df[0][i] == lineage_measured:
                    results[seed][ab]= predictions_df[2][i]
                    break
            
                if ab not in results[seed].keys():
                    results[seed][ab] = 0
    
    with open(dir_name + '/results.json', 'w') as f:
        json.dump(results, f)
    
    return 
    
# read json results
def read_json_results(dir_name): 
    with open(dir_name + '/results.json', 'w') as f:
        results = json.load(f)
    return results

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
