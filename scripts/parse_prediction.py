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

mapLocation = config.get('prediction', 'map_location')
predictionLocation = config.get('prediction', 'prediction_location')
resultsLocation = config.get('prediction', 'results_location')

print "----------------------------------------------------------------------------"
print "-Parse Prediction Files"
print "- Load config from:          ", sys.argv[1]
print "- Load map from:   ", mapLocation
print "- Load prediction from: ", predictionLocation
print "- Results output at:     ", resultsLocation
print "----------------------------------------------------------------------------"

with open(mapLocation, "r") as mapFile, open(predictionLocation, "r") as predictionFile, open(resultsLocation, "w", 0) as  resultsFile:
    
    #first line of prediction file is sample
    line = predictionFile.readline()
    file.write("Id,References\n")
    
    currentReferee = None
    refs = []

    for mapEntry, prediction in izip(mapFile, predictionFile):
        referee, reference = mapEntry.strip().split(":")
        label, confidence, invConfidence = prediction.strip().split()


        if referee != currentReferee:
            print "Next Referee"
            if currentReferee:
                predictionOut = [x[0] for x in refs]
                resultsFile.write(currentReferee + ", " + " ".join(predictionOut) + "\n")
            refs = []
            currentReferee = referee
        else:
            if label == "1":
                refs = papers.appendMax((reference, confidence), refs, 10)


    predictionOut = [x[0] for x in refs]
    resultsFile.write(currentReferee + ", " + " ".join(predictionOut) + "\n")