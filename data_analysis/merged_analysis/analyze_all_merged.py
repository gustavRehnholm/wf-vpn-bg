#!/usr/bin/env python3

'''
Copyright 2023 Gustav Rehnholm
SPDX-License-Identifier: Apache-2.0

To run:
python wf-attack-vpn/data_analysis/merged_analysis/analyze_all_merged.py -i merged_traffic/ -r analyse/...
'''

import argparse
import os

from merged_analysis import merged_analysis

ap = argparse.ArgumentParser(description ='Analyze all merged datasets that are in the provided folder')
ap.add_argument("-i", "--input"   , required = True , type = str, default = "", 
    help="root folder of the merged dataset")
ap.add_argument("-r", "--result", required = True , type = str,
    help="root folder of the overhead result")
ap.add_argument("-l", "--lenpkt", required = False , type = int, default = 5000,
    help="number of packets to analyse from the dataset")
ap.add_argument("-w", "--workers", required = False, type = int, default = 10, 
    help="number of workers for loading traces from disk")
ap.add_argument("-f", "--fold", required = False, type = str, default = "foreground_traffic/fold-0.csv", 
    help="Path to the fold file to use")
args = ap.parse_args()

def main():
    '''
    Analyze all merged datasets that are in the provided folder
    '''
    input_path  = args.input
    output_path = args.result

    dirs = os.listdir(input_path)
    for curr_dir in dirs:
        folder = f"{input_path}/{curr_dir}"
        os.system(f"mkdir {output_path}")
        merged_analysis(dir = folder, workers = args.workers, fold = args.fold, fname = f"{output_path}/{curr_dir}.txt", lenpkt = args.lenpkt)
    
if __name__ == "__main__":
    main()