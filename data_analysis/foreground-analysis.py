#!/usr/bin/env python3

import argparse
import os
from multiprocessing import Pool
import numpy as np
import sys
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt

# python wf-attack-vpn/data_analysis/foreground-analysis.py -d foreground_traffic/client


ap = argparse.ArgumentParser()
ap.add_argument("-d", required=True, default="", help="root folder of client/server dataset")
ap.add_argument("-w", required=False, type=int, default=10,
    help="number of workers for loading traces from disk")
ap.add_argument("--min", required=False, type=int, default=0, help="smallest packet size to consider")
args = vars(ap.parse_args())


def main():
    '''
    Analyze all capture files in a directory, generated by rds-collect
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
                    todo.append((os.path.join(root, name), name))

    p = Pool(args["w"])

    results = p.starmap(parse_trace, todo)

    # store statistics gathered from the file
    pkt_sec = get_pkt_sec(results)

    plot_bar(description_text = "mean pkt/sec", x_txt = "time (s)", y_txt = "packets", stat = pkt_sec)

    print("Saved the result")



def plot_bar(description_text, x_txt, y_txt, stat):
    '''
    plot of the foreground
    '''

    result_path = "fig/"
    file_name   = "foreground_stat"

    sns.barplot(data=stat, x=x_txt, y=y_txt)

    plt.title(description_text)

    fig = plt.gcf()
    os.system("rm " + str(result_path + file_name) + ".png")
    fig.savefig(result_path + file_name)

    plt.show()



def parse_trace(fname, name):
    '''
    Get mean packet per second, for the first 15 seconds from a foreground file, generated by Tobias Pulls
    Input:
        fname: path and name to the file which should be analyzed
        name: 
    Output:
        Tuple with statistics of the file
        Boolean               :  If it succeeded in gathering the files statistics
        timestamp             :  List of tiemstamps (in ns) of the packets
        fname                 :  The file that was analyzed
    '''

    with open(fname, "r") as f:
        timestamp = []
        for line in f:
            # parts: ["time(ns)", "direction", "size"]
            parts = line.strip().split(",")
            timestamp.append(int(parts[0]))

    return timestamp


def get_pkt_sec(timestamps):
    '''
    returns list of mean number of packets per second interval (from 0 to 15 seconds)
    '''
    upper     = []
    lower     = []
    ns        = 1000000000
    intervals = 15

    pkt_interval = [0] * intervals
    pkt_sec      = [0] * intervals
    traces       = len(timestamps)

    for i in range(0,intervals):
        lower.append(ns * i)
        upper.append(ns * (i + 1))

    # for every packet, in every trace, get which interval it resistent in
    for trace in timestamps:
        for packet in trace:
            # determine which interval it belongs to
            added_pkt = False
            for i in range(0,intervals):
                if packet > lower[i] and packet < upper[i]:
                    pkt_interval[i] += 1
                    added_pkt = True
                    break
            if not added_pkt:
                print("ERROR: packet could not be found in a interval")
                sys.exit()

    for j in pkt_interval:
        pkt_sec.append(j / traces)

    return pkt_sec

if __name__ == "__main__":
    main()
