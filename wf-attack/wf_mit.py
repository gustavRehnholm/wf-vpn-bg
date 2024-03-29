#!/usr/bin/env python3

import argparse
import os

'''
To run:
python wf-attack-vpn/wf-attack/wf_mit.py -app ...
'''

ap = argparse.ArgumentParser()
ap.add_argument("--app"   , required = True , type = str, default = "", 
    help="MIT application to use")
ap.add_argument("--len10k"   , required = False , type = bool, default = False, 
    help="How many packets per file to train for")
args = vars(ap.parse_args())

def main():
    '''
    wf-attack 10-fold merge for an MIT application
    '''
    print("Start wf attack on 10-fold")

    app = args["app"]
    

    if args["len10k"]:
        len = "-l"
        result_txt = "mit_10k"
    else:
        len = ""
        result_txt = "mit_5k"

    os.system(f"mkdir wf_result/{result_txt}/{app}")
    for i in range(0,10):
        os.system(f"mkdir wf_result/{result_txt}/{app}/fold_{i}")
        os.system(f"python wf-attack-vpn/wf-attack/wf-attack-dir.py -m merged_traffic/mit/{app}/fold_{i}/client/ -r wf_result/{result_txt}/{app}/fold_{i} -s 100 --epochs 30 {len}")
    
if __name__ == "__main__":
    main()