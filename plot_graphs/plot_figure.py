import sys
import os
import pandas            as pd
import matplotlib.pyplot as plt

def plot_figure(figure_dir ,x_label, y_label, sup_title = "", result_path  = "fig/" ):
    '''
    Plot a figure of the provided subplots (3 or 4)
    Structure of the folder: figure_dir -> subplot_dir -> csv files
    Args:
        figure_dir  - Required : path to folders, which contains the data to plot (List[str])
        x_label     - Required : label for the x axis             (str)
        y_label     - Required : label for the y axis             (str)
        sup_title   - Optional : title for the figure             (str)
        result_path - Optional : where to store the figure        (str)
    '''

    # paths to all subplots
    subplots_paths       = os.listdir(figure_dir)
    # how many subplots to show in the figure
    nr_subplots          = len(subplots_paths)
    # the datasets (as DataFrames) to show on each subplot [index per subplot][index per line/dataset]
    datasets_per_subplot = []
    # labels for each line [index per subplot][index per line/dataset label]
    labels_subplot_lines = []
    # subplot title is the same as the directories name
    subtitle = []

    for subplot_dir in subplots_paths:
        path = f"{figure_dir}/{subplot_dir}"
        datasets = []
        dataset_labels = []
        for csv_file in os.listdir(path):
            csv_path = f"{path}/{csv_file}"
            df = pd.read_csv(csv_path, usecols = ["th", "accuracy"], index_col = None)
            datasets.append(df)
            dataset_labels.append(csv_file)

        subtitle.append(subplot_dir)
        datasets_per_subplot.append(datasets)
        labels_subplot_lines.append(dataset_labels)

    # if 4 subplots per figure
    if nr_subplots == 4:
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))
        fig.subplots_adjust(top=0.8)

        # plot every subplot
        for index_subplot in range(4):
            # every line for the subplot
            for index_line in range(len(datasets_per_subplot[index_subplot])):   
                axes[(index_subplot%2),(index_subplot%1)].plot(datasets_per_subplot[index_subplot][index_line])
            axes[(index_subplot%2),(index_subplot%1)].set_title(subtitle[index_subplot])
            axes[(index_subplot%2),(index_subplot%1)].set_ylabel(y_label)
            axes[(index_subplot%2),(index_subplot%1)].set_xlabel(x_label)

        # save result and clear the plotting
        fig.suptitle(sup_title)
        fig.tight_layout()
        fig.savefig(f"{result_path}{sup_title}.png")
        plt.close(fig)

    # if 3 subplots per figure
    elif nr_subplots == 3:
        fig, axes = plt.subplots(3, 1, figsize=(10, 10))
        fig.subplots_adjust(top=0.8)

        for index_subplot in range(3):
            for index_line in range(len(datasets_per_subplot[index_subplot])):   
                #axes[index_subplot].plot(datasets_per_subplot[index_subplot][index_line])
                # data = datasets[j][["th", "accuracy"]]
                df = datasets_per_subplot[index_subplot][index_line]
                line_label = labels_subplot_lines[index_subplot][index_line]
                axes[index_subplot].plot(data = df[["th", "accuracy"]], label = line_label)
                print(df[["th", "accuracy"]])
                sys.exit()
            axes[index_subplot].set_title(subtitle[index_subplot])
            axes[index_subplot].set_ylabel(y_label)
            axes[index_subplot].set_xlabel(x_label)

        # save result and clear the plotting
        fig.suptitle(sup_title)
        fig.tight_layout()
        fig.savefig(f"{result_path}{sup_title}.png")
        plt.close(fig)

    else:
        print("ERROR: One must use 3 or 4 subplots per figure")
        sys.exit()

    return