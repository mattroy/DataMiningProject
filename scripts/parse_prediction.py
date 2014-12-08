#parse_prediction.py
#
# Parse the prediction file and  
# the map file.
#
#Data Mining Project
#CS6220 Fall 2014
#Team ELSAMAT

import sys
import os
import ConfigParser
import papers
from itertools import izip

config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

mapLocation = config.get('prediction', 'feature_map_location')
predictionLocation = config.get('prediction', 'eval_feature_location')
fullIdsLocation = config.get('prediction', 'full_id_list')
resultsLocation = config.get('prediction', 'results_location')

print "----------------------------------------------------------------------------"
print "-Parse Prediction Files"
print "- Load config from:     ", sys.argv[1]
print "- Load map from:        ", mapLocation
print "- Load prediction from: ", predictionLocation
print "- Results output at:    ", resultsLocation
print "----------------------------------------------------------------------------"

resultsFile = open(resultsLocation, "w", 0)

with open(mapLocation, "r") as mapFile, open(predictionLocation, "r") as predictionFile:
    
    #first line of prediction file is sample
    line = predictionFile.readline()
    resultsFile.write("Id,References\n")
    
    currentReferee = None
    refs = []
    doneRefs = {}

    for mapEntry, prediction in izip(mapFile, predictionFile):
        referee, reference = mapEntry.strip().split(":")
        label, confidence, invConfidence = prediction.strip().split()


        if referee != currentReferee:
            if currentReferee:
                predictionOut = [x[0] for x in refs]
                resultsFile.write(currentReferee + ", " + " ".join(predictionOut) + "\n")
                doneRefs[currentReferee] = 1
            refs = []
            currentReferee = referee
        else:
            if label == "1":
                refs = papers.appendMax((reference, confidence), refs, 10)


    predictionOut = [x[0] for x in refs]
    resultsFile.write(currentReferee + ", " + " ".join(predictionOut) + "\n")
    doneRefs[currentReferee] = 1

with open(fullIdsLocation, "r") as fullIds:
    for line in fullIds:
        evalId, preds = line.split(",")
        if evalId not in doneRefs:
            resultsFile.write(evalId + ", "  + "\n")            
