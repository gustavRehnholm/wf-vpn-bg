#!/bin/bash

# get print for all 5k mit results
# To run: 
#./wf-attack-vpn/plot_graphs/scripts/mit_5k_print.sh

# structure result, for cleaner print
python wf-attack-vpn/plot_graphs/result_print.py --app youtube    -r mit_5k_print -i mit_5k
python wf-attack-vpn/plot_graphs/result_print.py --app netflix    -r mit_5k_print -i mit_5k
python wf-attack-vpn/plot_graphs/result_print.py --app vimeo      -r mit_5k_print -i mit_5k
python wf-attack-vpn/plot_graphs/result_print.py --app voip       -r mit_5k_print -i mit_5k
python wf-attack-vpn/plot_graphs/result_print.py --app rdp        -r mit_5k_print -i mit_5k
python wf-attack-vpn/plot_graphs/result_print.py --app skype-chat -r mit_5k_print -i mit_5k
python wf-attack-vpn/plot_graphs/result_print.py --app ssh        -r mit_5k_print -i mit_5k

# get graph of the new cleaner structure
python wf-attack-vpn/plot_graphs/plot_all.py -r wf_result/mit_5k_print/ -g fig/mit_5k/ -w 10 --ylim_lower 0

# get overhead
python wf-attack-vpn/data_analysis/analyze_all_merged.py -i merged_traffic/mit/youtube    -r overhead/youtube_5k
python wf-attack-vpn/data_analysis/analyze_all_merged.py -i merged_traffic/mit/netflix    -r overhead/netflix_5k
python wf-attack-vpn/data_analysis/analyze_all_merged.py -i merged_traffic/mit/youtube    -r overhead/youtube_5k
python wf-attack-vpn/data_analysis/analyze_all_merged.py -i merged_traffic/mit/vimeo      -r overhead/vimeo_5k
python wf-attack-vpn/data_analysis/analyze_all_merged.py -i merged_traffic/mit/voip       -r overhead/voip_5k
python wf-attack-vpn/data_analysis/analyze_all_merged.py -i merged_traffic/mit/rdp        -r overhead/rdp_5k
python wf-attack-vpn/data_analysis/analyze_all_merged.py -i merged_traffic/mit/skype-chat -r overhead/skype-chat_5k
python wf-attack-vpn/data_analysis/analyze_all_merged.py -i merged_traffic/mit/ssh        -r overhead/ssh_5k