# data analysis
This part is for scripts that extract information about the datasets used. They are sorted after which dataset they analyze, background, foreground, merged or WF result (which is not to present graphs)

## background traffic analysis
The background does both consist of unparsed Twitch data, which can be useful if rds-collect will be used more in the future (so one can analyse the data, and remove unnecesary parts, before making the trouble of parsing it).

### create_background_dataset.py
Creates a subset of traffic from dataset generated from the rds-collect. Can be useful if one will generate more data from that tool, to remove unwanted parts. 

### rds_collect_analysis.py
Graphs of dataset generated by rds-collect, with an empathize on packets per second

### rds_collect_analysis_table.py
Statistic table for a dataset, generated by rds-collect


## foreground analysis
with the code foreground_analysis.py, one can get a table of packets per second interval for all (or induvidual files) of the foreground dataset. Have been used to find delays at the start of foreground datasets. 


## Merged dataset analysis
The merged dataset, can be analyzed for overhead, by runing analyze_all_merged.py, which will analyse all files in a directory. The analysis is performed by merged_analysis.py

### wf result
To get the median accuracy of the DF and TIk-Tok results