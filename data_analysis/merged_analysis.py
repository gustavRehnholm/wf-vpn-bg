#!/usr/bin/env python3

import argparse
import os
from multiprocessing import Pool
import numpy as np
import sys

'''
To run:
python wf-attack-vpn/data_analysis/merged_analysis.py -d twitch_rnd_40
'''

ap = argparse.ArgumentParser()
ap.add_argument("-d"   , required = True , type = str, default = "", 
    help="root folder of the merged dataset")
ap.add_argument("-w"   , required = False, type = int, default = 10, 
    help="number of workers for loading traces from disk")
ap.add_argument("--fold", required = False, type = str, default = "foreground_traffic/fold-0.csv", 
    help="Path to the fold file to use")
args = vars(ap.parse_args())
ap.add_argument("--fname", required = False, type = str, default = "stdout/merged_analysis.txt", 
    help="Text file to store the result in")
args = vars(ap.parse_args())


def main():
    '''
    Run analysis of one merged dataset from the terminal
    '''
    merged_analysis(dir = args["d"], workers = args['w'], fold = args["fold"], fname = args['fname'])


def merged_analysis(dir, workers = 10, fold = "foreground_traffic/fold-0.csv", fname = "stdout/merged_analysis.txt"):
    '''
    Analyze merged dataset, to see how much of the packets are from the foreground and background
    Is done on the dataset as a whole, and its subsets (testing, validation and training)
    Args:
        dir      - Required : root folder of the merged dataset              (str)
        workers  - Optional : number of workers for loading traces from disk (int)
        fold     - Optional : The fold file to use                           (str)
        fname    - Optional : Text file to store the result in               (str)
    '''

    print(f"walking directory {args['d']}, this might take some time...")
    print("")

    # walk the dataset folder
    todo = []
    dirs = os.listdir(args["d"])

    # for each webpage dir
    for curr_dir in dirs:
        folder = args['d'] + "/" + curr_dir
        # for all log files for each webpage
        for root, dirs, files in os.walk(folder, topdown = False):
            for name in files:
                if ".log" in name:
                    todo.append(os.path.join(root, name))

    merged_train_files = []
    merged_valid_files = []
    merged_test_files = []
    df_fold = pd.read_csv(args["fold"])

    # For every log file in the foreground, make sure that there is an correlating log file to store the parsed result
    for x in range(0, len(df_fold['log'])):
        if(df_fold['is_train'][x] == True): 
            merged_train_files.append(os.path.join(dir_merged, df_fold['log'][x]))
        elif(df_fold['is_valid'][x] == True): 
            merged_valid_files.append(os.path.join(dir_merged, df_fold['log'][x]))
        elif(df_fold['is_test'][x] == True): 
            merged_test_files.append(os.path.join(dir_merged, df_fold['log'][x]))
        else:
            print("ERROR: the file " + df_fold['log'][x] + "does not have a determined usage")
            print("Aborting program")
            sys.exit()


    p = Pool(args["w"])

    input_all   = []
    input_train = []
    input_valid = []
    input_test  = []
    for file in todo:
        input_all.append( (file, 1) )
        if file in merged_train_files:
            input_train.append( (file, 1) )
        elif file in merged_valid_files:
            input_valid.append( (file, 1) )
        elif file in merged_test_files:
            input_test.append( (file, 1) )
        else:
            print(f"the file {file} does not belong to any subset")
            sys.exit()

    # to test with one packet
    #input = [("foreground_traffic/client/0/0000-0001-0047.log",intervals)]

    file_stats_all   = p.starmap(percent_foreground, input_all)
    file_stats_train = p.starmap(percent_foreground, input_train)
    file_stats_valid = p.starmap(percent_foreground, input_valid)
    file_stats_test  = p.starmap(percent_foreground, input_test)

    np_stat_all   = np.array(file_stats_all)
    np_stat_train = np.array(file_stats_train)
    np_stat_valid = np.array(file_stats_valid)
    np_stat_test  = np.array(file_stats_test)

    try:
        open(args['fname'], 'w').close()
        with open(args['fname'], "a") as f:
            # print some descriptive statistics
            print("Percentage of the packet that comes from the foreground:", file=f)
            print(stat_txt("All subsets" , np_stat_all), file=f)
            print(stat_txt("Training subset" , np_stat_train), file=f)
            print(stat_txt("Validation subset" , np_stat_valid), file=f)
            print(stat_txt("Testing subset" , np_stat_test), file=f)
    except:
        print("ERROR while calculating stastics")
        return
    

def percent_foreground(fname, dir_index):
    '''
    Get the percentage of how much of the files lines comes from the foreground dataset
    '''
    background_packets = 0
    foreground_packets = 0
    with open(fname, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            try:
                dir = parts[dir_index]
            except:
                print(f"ERROR: could not extract line: {parts}, ending program")
                sys.exit()
            if dir == "sb" or dir == "rb":
                background_packets += 1
            elif dir == "s" or dir == "r":
                foreground_packets += 1
            else:
                print(f"ERROR: direction {dir} is not valid")
                sys.exit()

    percent_foreground = (foreground_packets)/(background_packets + foreground_packets)
    percent_foreground = percent_foreground * 100
    return percent_foreground


def stat_txt(description_text, np_array):
    '''
    format how to print statistics 
    Input:
        description_text: short string (1-3 words) to describe what the statistics is for 
        np_array        : what to show statistics for 
    Output:
        string to print
    '''
    txt = "{description:>13}: {mean:>15.2f} +- {std:>15.2f}, median: {median:>15.2f},  min: {min:>15.2f}, max: {max:>15.2f}"

    return txt.format(description = description_text   , mean = np.mean(np_array), std = np.std(np_array), 
                      median      = np.median(np_array), min  = np.min(np_array) , max = np.max(np_array))

if __name__ == "__main__":
    main()