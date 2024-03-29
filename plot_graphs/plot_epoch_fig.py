import sys
import os
import pandas            as pd
import matplotlib.pyplot as plt
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-r"   , required = True , type = str, default = "wf_result", 
    help="root folder of the DF result")
ap.add_argument("-t"   , required = True , type = str, default = "", 
    help="title")
args = vars(ap.parse_args())

'''
python wf-attack-vpn/plot_graphs/plot_epoch_fig.py -r wf_result/twitch/twitch_rnd_epoch      -t twitch_epoch
python wf-attack-vpn/plot_graphs/plot_epoch_fig.py -r wf_result/twitch/twitch_div_rnd_epoch  -t twitch_split_epoch
'''

def main():
    plot_figure(figure_dir = args["r"], sup_title = args["t"])


def plot_figure(figure_dir , x_label = 'Threshold', y_label = 'Accuracy', y_lim = [0.5, 1], sup_title = "", result_path  = "fig/twitch" ):
    '''
    Plot a figure of the provided subplots (3 or 4)
    Structure of the folder: subplot_dir -> csv files
    Args:
        figure_dir  - Required : path to folders, which contains the data to plot (List[str])
        x_label     - Required : label for the x axis             (str)
        y_label     - Required : label for the y axis             (str)
        y_lim       - Optional : limitations on the y-axis        ([int, int])
        sup_title   - Optional : title for the figure             (str)
        result_path - Optional : where to store the figure        (str)
    '''
    SIZE_PER_SUBGRAPH = 4
    # paths to all subplots
    #subplots_paths       = os.listdir(figure_dir)
    #subplots_paths.sort()
    subplots_paths = ["", "", ""]
    subplots_paths[0] = "_2h_epoch_60"
    subplots_paths[1] = "_2h_epoch_300"
    subplots_paths[2] = "_2h_epoch_1000"
    # how many subplots to show in the figure
    nr_subplots          = len(subplots_paths)
    # the datasets (as DataFrames) to show on each subplot [index per subplot][index per line/dataset]
    datasets_per_subplot = []
    # labels for each line [index per subplot][index per line/dataset label]
    labels_subplot_lines = []
    # subplot title is the same as the directories name
    subtitle = []
    # 
    markers_list = ['x','o','v','^','<', '1', 'P', '+', 'd', '|', '2', '3', '4']

    for subplot_dir in subplots_paths:
        path = f"{figure_dir}/{subplot_dir}"
        datasets = []
        dataset_labels = []
        csv_files = os.listdir(path)
        csv_files.sort()
        for csv_file in csv_files:
            csv_path = f"{path}/{csv_file}"
            df = pd.read_csv(csv_path, usecols = ["th", "accuracy"], index_col = None)
            datasets.append(df)
            fname = csv_file.split('.')[0]
            dataset_labels.append(fname)

        subtitle.append(subplot_dir)
        datasets_per_subplot.append(datasets)
        labels_subplot_lines.append(dataset_labels)

    # if 4 subplots per figure (2x2)
    if nr_subplots == 4 or nr_subplots == 10:
        nrows = round(nr_subplots/2)
        ncols = 2
        fig, axes   = plt.subplots(nrows = nrows, ncols = ncols, figsize=(SIZE_PER_SUBGRAPH * ncols, SIZE_PER_SUBGRAPH * nrows))
        fig.subplots_adjust(top=0.8)

        # plot every subplot
        index_subplot = -1
        for index_subplot_row in range(nrows):
            for index_subplot_column in range(ncols):
                index_subplot += 1
                # every line for the subplot
                for index_line in range(len(datasets_per_subplot[index_subplot])): 
                    df         = datasets_per_subplot[index_subplot][index_line]
                    line_label = labels_subplot_lines[index_subplot][index_line]  
                    axes[index_subplot_row, index_subplot_column].plot(df["th"], df["accuracy"], label = line_label, marker = markers_list[index_line], linewidth=2)

                axes[index_subplot_row, index_subplot_column].set_title(subtitle[index_subplot])
                axes[index_subplot_row, index_subplot_column].set_ylabel(y_label)
                axes[index_subplot_row, index_subplot_column].set_xlabel(x_label)
                axes[index_subplot_row, index_subplot_column].legend()
                axes[index_subplot_row, index_subplot_column].set_ylim(y_lim)
                axes[index_subplot_row, index_subplot_column].set_xlim([0, 1])

        # save result and clear the plotting
        fig.suptitle(sup_title)
        fig.tight_layout()
        fig.savefig(f"{result_path}/{sup_title}.png")
        plt.close(fig)

    # subgraphs in 1 column (1 X nr_subplots)
    else:
        height    = SIZE_PER_SUBGRAPH
        width     = SIZE_PER_SUBGRAPH * nr_subplots
        fig, axes = plt.subplots(nrows = 1, ncols = nr_subplots, figsize=(width, height))
        fig.subplots_adjust(top=0.8)

        for index_subplot in range(nr_subplots):
            for index_line in range(len(datasets_per_subplot[index_subplot])):   
                df         = datasets_per_subplot[index_subplot][index_line]
                line_label = labels_subplot_lines[index_subplot][index_line]
                axes[index_subplot].plot(df["th"], df["accuracy"], label = line_label, marker = markers_list[index_line], linewidth=2)

            axes[index_subplot].set_title(subtitle[index_subplot])
            axes[index_subplot].set_ylabel(y_label)
            axes[index_subplot].set_xlabel(x_label)
            axes[index_subplot].legend()
            axes[index_subplot].set_ylim(y_lim)
            axes[index_subplot].set_xlim([0, 0.99])
        # save result and clear the plotting
        fig.suptitle(sup_title)
        fig.tight_layout()
        fig.savefig(f"{result_path}/{sup_title}.png")
        plt.close(fig)

    return


if __name__ == "__main__":
    main()