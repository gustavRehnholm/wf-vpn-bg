#!/usr/bin/env python

import os
from os import walk
from os import path
from re import search
import time
import pandas as pd

def main():
    '''
    modified version of rds-collect, where the program ends properly
    '''    

    hours = 60*60
    minutes = 60
    nanoseconds = 1000000000
    saveTime = time.time()
    IP_host = '10.88.0.9'
    filesToParseDir = "captures_clean"
    parsedFilesDir = "merged_traffic/old_twitch"
    crossFilesDir = "foreground_traffic/client"
    excelFile = "foreground_traffic/fold-0.csv"
    header = 40

    deviationTime = 0
    crossFilePath = []
    newFilePath = []
    newFile = []
    crossLine = []
    filesToParse = []

    trainFiles = []
    validFiles = []
    testFiles = []
    parsedTrainFiles = []
    parsedValidFiles = []
    parsedTestFiles = []

    masterFile = os.path.join(os.getcwd(), filesToParseDir)
    parsedDirectory = os.path.join(os.getcwd(), parsedFilesDir)
    directory = os.path.join(os.getcwd(), crossFilesDir)

    for (dirpath, dirnames, filenames) in walk(masterFile, topdown=True):
        for files in filenames:
            filesToParse.append(os.path.join(masterFile, files))
        print("Files to parse: ", len(filesToParse))
    print("Setting up directories")
    for (dirpath, dirnames, filenames) in walk(directory, topdown=True):
        for dirs in dirnames:
            try: 
                os.mkdir(os.path.join(parsedDirectory, dirs))
            except: 
                print("File and directory exists!") 

    #----------------------limited data data set sorting--------------------

    df = pd.read_csv(excelFile)
    dfFormat = ['log', 'is_train', 'is_valid', 'is_test']
    dfFiles = df[dfFormat]

    for x in range(0, len(dfFiles['log'])):
        if(dfFiles['is_train'][x] == True): 
            parsedTrainFiles.append(os.path.join(parsedDirectory, dfFiles['log'][x]))
            trainFiles.append(os.path.join(directory, dfFiles['log'][x]))
        elif(dfFiles['is_valid'][x] == True): 
            parsedValidFiles.append(os.path.join(parsedDirectory, dfFiles['log'][x]))
            validFiles.append(os.path.join(directory, dfFiles['log'][x]))
        else: 
            parsedTestFiles.append(os.path.join(parsedDirectory, dfFiles['log'][x]))
            testFiles.append(os.path.join(directory, dfFiles['log'][x]))

    #-----------------------------------------------------------------------

    print("Starting parse")
    print("trainFiles len = ", len(trainFiles))
    filesToParse.sort()
    print("filesToParse len  = ", len(filesToParse), "\n")
    while(len(trainFiles) > 0):
        for fileToParsePath in filesToParse:
            print("New file to parse: ", os.path.basename(fileToParsePath))
            with open(fileToParsePath, 'r') as fileToParse:
                print("Opening ", os.path.basename(fileToParsePath))
                
                print("testingFiles    left: ", len(testFiles))
                print("validationFiles left: ", len(validFiles))
                print("trainingFiles   left: ", len(trainFiles))
                print("Lines left in crossfile: ", len(crossLine))
                print("\n")

                for parseLine in fileToParse: #Reading line by line from the master file since it might be to large to do readlines() on
                    splitParseLine = parseLine.split("\t")
                    parseLineTime = splitParseLine[0].split('.')
                    totalTime = int(parseLineTime[0]) * nanoseconds
                    totalTime += int(parseLineTime[1])

                    directionSplit = splitParseLine[1].split(',')
                    
                    #-------------------limited files open test, valid then training-----------------------
                    if (not len(crossLine) and len(testFiles) > 0): #Check if it's time to preload a new file
                        deviationTime = totalTime #make deviation to match start at zero

                        crossFile = open(testFiles[0], 'r') #File from Tobias set
                        testFiles.pop(0)
                        
                        crossLine = crossFile.readlines()
                        crossFile.close()

                        newFile = open(parsedTestFiles[0], 'a') #What we write to
                        print("Printing to new test set file ", os.path.basename(parsedTestFiles[0]))
                        parsedTestFiles.pop(0)

                    elif (not len(crossLine) and len(validFiles) > 0): #Check if it's time to preload a new file
                        deviationTime = totalTime #make deviation to match start at zero

                        crossFile = open(validFiles[0], 'r') #File from Tobias set
                        validFiles.pop(0)
                        
                        crossLine = crossFile.readlines()
                        crossFile.close()

                        newFile = open(parsedValidFiles[0], 'a') #What we write to
                        print("Printing to new validation set file", os.path.basename(parsedValidFiles[0])) 
                        parsedValidFiles.pop(0)

                    elif (not len(crossLine) and len(trainFiles) > 0):
                        deviationTime = totalTime #make deviation to match start at zero

                        crossFile = open(trainFiles[0], 'r') #File from Tobias set
                        trainFiles.pop(0)
                        
                        crossLine = crossFile.readlines()
                        crossFile.close()

                        newFile = open(parsedTrainFiles[0], 'a') #What we write to
                        print("Printing to new training set file ", os.path.basename(parsedTrainFiles[0]))
                        parsedTrainFiles.pop(0)
                    # ADDED, WAS NOT HERE ORIGINAL;
                    elif len(crossLine) == 0:
                        # Done with the parsing
                        print("Have injected all web traffic with noise")
                        print("Ending the program")
                        return

                    #-------------------------rewrite this shit code above to take less lines, this looks abyssmal---------------

                    finalTime = totalTime - deviationTime

                    # TODO: add continue for when packet size is missing but IP exists. 
                    if(directionSplit[0] == ''):
                        continue
                    if (directionSplit[0] == IP_host):
                        direction = 's'
                    elif(directionSplit[1] == IP_host):
                        direction = 'r'
                    else:
                        checkIfLocal = directionSplit[0].split('.')
                        if checkIfLocal[0] == '10':
                            IP_host = directionSplit[0]
                        else: IP_host = directionSplit[1]

                    #if(int(splitParseLine[2]) > 1420): splitParseLine[2] = '1420\n'

                    # ADDED, WAS NOT HERE ORIGINAL; but the script crashes if it does not
                    try:
                        splitCrossLine = crossLine[0].split(",")
                    except:
                        print("Cross line is empty")
                        continue

                    packetSize = str(int(splitParseLine[2])-header)

                    if(finalTime < int(splitCrossLine[0])):
                        newFile.writelines([str(finalTime), ",", direction, ",", packetSize, "\n"])
                        saveTime = totalTime
                    else:
                        newFile.writelines(crossLine[0])
                        crossLine.pop(0)

                print("Out of lines in ", os.path.basename(fileToParsePath), "\nClosing...")
                deviationTime = 0
                fileToParse.close()
            if(len(testFiles) > 0 and len(validFiles) > 0):
                print("Popping ", os.path.basename(filesToParse[0]))
                filesToParse.pop(0)
                print("Now first one is: ", os.path.basename(filesToParse[0]), "\n")
            else: print("We stopped removing files")

# run main 
if __name__=="__main__":
    main()