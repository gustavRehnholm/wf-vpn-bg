#!/usr/bin/python3

import pandas as pd
import os
import shutil
from multiprocessing import Pool

def combine(dir_train, dir_test, dir_dest, f_fold = 0, workers = 10):
    '''
    Args:
        dir_train - Required : path to dataset to use for training and validation (str)
        dir_test  - Required : path to dataset to use for testing                 (str)
        dir_dest  - Required : path for the result                                (str)
        f_fold    - Optional : which fold file to use for the foreground [0, 9]   (int)
        workers   - Optional : number of workers, multiprocessing                 (int)
    '''

    FOLD_CSV = dir_train + "/fold-" + str(f_fold) + ".csv"

    # list of tuples of the pair (src, dst)
    input = []

    # clean old results if their is any
    if os.path.exists(dir_dest):
        shutil.rmtree(dir_dest)
    # create structure to be in the merged folder (client with results, and fold file)
    os.mkdir(dir_dest)
    os.mkdir(f"{dir_dest}/client")
    os.system(f"cp {FOLD_CSV} {dir_dest}")
    
    # The naming structure between the training set and result should be the same
    for (dirpath, dirnames, filenames) in os.walk(dir_train, topdown = True):
        for dirs in dirnames:
            client_path = os.path.join(dir_dest, "client")
            curr_path = os.path.join(client_path, dirs)
            if not os.path.exists(curr_path):
                os.mkdir(curr_path)

    df_fold = pd.read_csv(FOLD_CSV)

    # get paths to copy from and to
    for x in range(0, len(df_fold['log'])):
        # train and validation picked from the attackers dataset
        if(df_fold['is_train'][x] == True) or (df_fold['is_valid'][x] == True): 
            src = os.path.join(dir_train, "client", df_fold['log'][x])
        # testing outsides the attackers dataset
        elif(df_fold['is_test'][x] == True): 
            src = os.path.join(dir_test, "client", df_fold['log'][x])
        else:
            print(f"ERROR: the file {df_fold['log'][x]} does not have a determined usage")
            print("Each packet most be for training, validation or testing")
            print("Aborting program")
            return

        dst = os.path.join(dir_dest, "client", df_fold['log'][x])
        input.append((src, dst))

    p = Pool(workers)
    results = p.starmap(shutil.copyfile, input)

    if False in results:
        print("ERROR: failed to inject")
        return False
    else:
        return True

if __name__=="__main__":
    main()