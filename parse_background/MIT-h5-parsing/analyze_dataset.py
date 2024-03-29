#!/usr/bin/python3

'''
To run:
python wf-attack-vpn/parse_background/MIT-h5-parsing/analyze_dataset.py

python wf-attack-vpn/parse_background/MIT-h5-parsing/analyze_dataset.py --input mit/parsed_streaming/ --output fig/mit_streaming_analysis/ 
'''

from multiprocessing import Pool
import pandas            as pd
import seaborn           as sns
import numpy             as np
import matplotlib.pyplot as plt
import os
import sys
import json
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("--input"  , required = False, default = "mit/parsed_app/"   , type = str, help = "Directory for the files to analyze")
ap.add_argument("--output" , required = False, default = "fig/mit_analysis/" , type = str, help = "Directory to store the result")
ap.add_argument("--workers", required = False, default = 10                  , type = int, help = "Workers for multiprocessing")
args = vars(ap.parse_args())


def main():
    '''
    Analyze the provided background traffic
    '''
    print("Start analyzing background")
    analyze_dataset(dir_input   = args['input'],
                    dir_output  = args['output'],
                    workers     = args['workers'])
    return


def analyze_dataset(dir_input = "mit/parsed_app/", dir_output = "fig/mit_analysis/", workers = 10):
    '''
    Analyze the parsed Twitch dataset

    Args:
        dir_input  - Optional : Path to the captures to analyze (str)
        dir_output - Optional : Path to the twitch analysis     (str)
        workers    - Optional : Workers for multiprocessing     (int)
    '''

    # each application capture from MIT
    input_files = os.listdir(dir_input)
    input = []
    for curr_file in input_files:
        fname_with_extension = os.fsdecode(curr_file)
        path = dir_input + "/" + fname_with_extension
        fname_without_extension = fname_with_extension.split('.')[0]
        input.append((path, fname_without_extension))

    p = Pool(workers)

    # list of pkt/s for each second interval
    print("Start extracting pkt/sec for each sec interval")
    time_lists = p.starmap(timestamps_capture, input)

    # plot a line for min, max and mean
    plot_analysis_captures(captures_pkt_s = time_lists,  title = "MIT_app_analysis", result_path = dir_output)

    return


def timestamps_capture(path_file2analyze, fname):
    '''
    get list of number of packet, each second, for the file

    Args:
        path_file2analyze - Required : path to the file                             (str)
        fname             - Required : associated file name (so it do not get lost) (str)
    Return:
        time_list   : list of packets/sec for each second
        index       : same index as the one from args
        upper_limit : the highest second interval a packet was sent in 
    '''
    NS_PER_SEC       = 1000000000
    TUPLE_TIME_INDEX = 0

    # the background packets as a list of tuples (better performance than working with the dataframe)
    df               = pd.read_hdf(path_file2analyze, key = "df")
    background_tuple = list(df.itertuples(index=False, name=None))
    len_tuple        =  len(background_tuple)
    print(f"number of packets in the file {fname}: {len_tuple}")
    time_list        = [0]
    # keep track of current packet and time interval
    interval_index   = 0
    lower_limit = interval_index     * NS_PER_SEC
    upper_limit = (interval_index+1) * NS_PER_SEC

    
    # which timestamp the packet is sent in
    tuple_index = 0
    time_stamp   = int(background_tuple[tuple_index][TUPLE_TIME_INDEX])
    tuple_index += 1

    while tuple_index < len_tuple:
        # if timestamp is in the next intervall
        if time_stamp >= upper_limit:
            time_list.append(0)
            interval_index += 1
            # advance the time with the duration of the next packet
            lower_limit = interval_index     * NS_PER_SEC
            upper_limit = (interval_index+1) * NS_PER_SEC
        # advance the interval
        else:
            # one more packet this second
            time_list[interval_index] += 1
            time_stamp                += int(background_tuple[tuple_index][TUPLE_TIME_INDEX])
            tuple_index               += 1


    result_dic = {"pkt_s": time_list, "fname": fname}

    with open(f'tmp/{fname}.txt', 'w') as file:
        file.write(json.dumps(result_dic))

    return result_dic


def plot_analysis_captures(captures_pkt_s, title = "MIT_app_analysis", result_path = "fig/"):
    '''
    Plot a graph to show how the captured data from rds-collect behavior
    Args:
        app_pkt_s     - Required : list of each                   (List[dict{pkt_s, fname}])
        title         - Optional : title of the figure            (str)
        result_path   - Optional : Where to store the figure      (str)

    '''
    if len(captures_pkt_s) == 10:
        nrows = 5
        ncols = 2
        fig, axes = plt.subplots(nrows = nrows, ncols = ncols, figsize=(10, 10))
        fig.subplots_adjust(top=0.8)

        capture_index = 0
        for row_index in range (nrows):
            for col_index in range (ncols):
                axes[row_index, col_index].plot(captures_pkt_s[capture_index]["pkt_s"])
                axes[row_index, col_index].set_title(captures_pkt_s[capture_index]["fname"])
                axes[row_index, col_index].set_ylabel('pkt/s')
                axes[row_index, col_index].set_xlabel('time(sec)')
                capture_index += 1

    elif len(captures_pkt_s) == 3:
        nrows = 3
        ncols = 1
        fig, axes = plt.subplots(nrows = nrows, ncols = ncols, figsize=(10, 10))
        fig.subplots_adjust(top=0.8)

        for row_index in range (nrows):
            axes[row_index].plot(captures_pkt_s[row_index]["pkt_s"])
            axes[row_index].set_title(captures_pkt_s[row_index]["fname"])
            axes[row_index].set_ylabel('pkt/s')
            axes[row_index].set_xlabel('time(sec)')
            axes[row_index].set(xlim=(0, 3500), ylim=(0, 12000))
    else:
        print(f"ERROR: invalid number of graphs to plot {len(captures_pkt_s)}")
        return


    # save result and clear the plotting
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(f"{result_path}{title}.png")
    plt.close(fig)

    return

if __name__=="__main__":
    main()