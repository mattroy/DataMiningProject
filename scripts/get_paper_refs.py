#get_paper_refs.py
#
#This script builds a list of the counts that a paper has receieved.
#
#Data Mining Project
#CS6220 Fall 2014
#Team ELSAMAT

import sys
import os
import ConfigParser
import papers

config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

trainingLocation = config.get('data_analysis', 'training_location')
outputLocation = config.get('data_analysis', 'paper_ref_count_location')

trainingData = papers.Corpus()
trainingData.readCorpus(trainingLocation)

print "----------------------------------------------------------------------------"
print "-Parse Prediction Files"
print "- Load config from:     ", sys.argv[1]
print "- Load training from:   ", trainingLocation
print "- Results output at:    ", outputLocation
print "----------------------------------------------------------------------------"


with open(outputLocation, "w", 0) as f:
    for paperId in trainingData.paperReferenceCount:
        f.write(paperId + ":" + str(trainingData.paperReferenceCount[paperId]) + "\n")