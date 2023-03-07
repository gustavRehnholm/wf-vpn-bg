#!/usr/bin/python3

'''
Convert the raw log files to dataframes, and store them with h5
That way, they will be faster to handle

touch stdout/log_2_h5.txt
python wf-attack-vpn/Parse_noise/KAU-twitch-parsing/log_2_h5.py | tee stdout/log_2_h5.txt
'''

import pandas as pd
import os

def main():
    print("Start converting twitch traffic")
    # parsed noise files
    DIR_input = "captures/"
    # the captures in h5 format
    DIR_output = "twitch/raw_captures_h5/"

    COL_NAMES =  ['time', 'sender', 'receiver', 'size']

    # clean the prevoius content of the 
    os.system("rm -f -r " + DIR_output)
    os.system("mkdir " + DIR_output)


    index = 0
    for file in os.listdir(DIR_input):

        filename = os.fsdecode(file)
        if not filename.endswith(".log"): 
            print("ERROR: the file (" + str(filename) + ") should not be part of the directory")
            print("Only log files should be part of the twitch dataset")
            print("Aborting the program")
            return

        index += 1
        print("")
        print("converting file " + str(index) + "/1370: " + str(filename))
        print("")

        path = DIR_input + filename
        df = pd.read_csv(path, names = COL_NAMES)

        df_file_name = DIR_output + filename.rsplit('.', 1)[0] + '.h5'
        df.to_hdf(df_file_name, mode = "w", key = "df")

# run main 
if __name__=="__main__":
    main()