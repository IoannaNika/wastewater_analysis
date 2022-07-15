import os
import glob
import pandas as pd
import sys
import argparse
import fnmatch
from csv import writer



def main():
    parser = argparse.ArgumentParser(description="Merge fasta and metadata files")
    parser.add_argument('--dir', dest = 'dir', required=True, type=str, help="data directory, merges metadata and fasta contained in the directory and its subdirectories")
    args = parser.parse_args()

    # go to directory where the sub dirs and the files are.
    os.chdir(args.dir)
    curr_dir = os.getcwd()
    
    mt = "metadata.tsv"
    fst = "sequences.fasta"

    #Create metadata file
    if os.path.exists(mt):
        os.remove(mt)
    
    #Create fasta file
    if os.path.exists(fst):
        os.remove(fst)
    
    metadata = open("metadata.tsv", "x")
    metadata = open("metadata.tsv", "a")

    #Create fasta file
    fasta = open("sequences.fasta", "x")
    fasta = open("sequences.fasta", "a")
    
    for directory, subdir, file in os.walk(curr_dir):

        for item in file:

            currentFile=os.path.join(directory, item)

            if fnmatch.fnmatch(item, '*.fasta'):
                with open(currentFile) as fl:
                    for line in fl:
                        fasta.write(line)          
                    
            if fnmatch.fnmatch(item, '*.tsv'):
                with open(currentFile) as fl:
                    lines = fl.readlines()
                    if os.stat("metadata.tsv").st_size != 0:
                        lines = lines[1:]

                    for line in lines:
                        metadata.write(line)
                
        
    metadata.close()
    fasta.close()

    return

if __name__ == "__main__":
    sys.exit(main())
