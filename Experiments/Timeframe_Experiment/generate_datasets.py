from os import curdir
import sys
from utils.helper_functions import *
import argparse


def main():
    parser = argparse.ArgumentParser(description="Merge fasta and metadata files")
    parser.add_argument('--data', dest = 'data', required=False, default="Europe,North_America,Global,Asia", type=str, help="comma seperated strings for the name of datasets to be used")
    args = parser.parse_args()

    datasets = args.data.split(",")
    dates = [("2020-01-01", "2022-06-08"), ("2021-01-01", "2022-06-08"), ("2021-06-01", "2022-06-08"), ("2022-01-01", "2022-06-08"), ("2022-01-01", "2022-06-08"), ("2022-06-01", "2022-06-08")]

    for dataset in datasets:
        path = "data/Timeframe_Experiments/{}_next_regions_download_6_Jul_2022/".format(dataset)
        for date in dates:
            start_date = date[0]
            end_date = date[1]
            outdir = "data/Timeframe_Experiments/{}_next_regions_download_6_Jul_2022/{}_till_{}".format(dataset, start_date,end_date)
            try:
                os.mkdir(outdir)
            except:
                pass
            filter_dataset_by_date(path + "metadata.tsv", path + "sequences.fasta", outdir, start_date, end_date)

    return


if __name__ == "__main__":
    sys.exit(main())
