#!/bin/bash
# Test to get the start of the foreground traffic, by testing against the capture file with the highest density of packets

# to run:
# ./wf-attack-vpn/data_analysis/tests/twitch_5_01.sh

# merge 
python wf-attack-vpn/merge_traffic/main.py -f foreground_traffic -b background_traffic/test/twitch_largest.h5 -m merged_traffic/test/5_10/twitch_1 --ffold 0 -w 5

# analysis
python wf-attack-vpn/data_analysis/merged-foreground-ratio.py -d merged_traffic/test/5_10/twitch_largest_1
