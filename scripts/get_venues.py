#get_venues.py
#
#This is a simple heuristic baseline for 
#predicting references to papers.
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
outputLocation = config.get('data_analysis', 'output_location')

trainingData = papers.Corpus()
trainingData.readCorpus(trainingLocation)

with open(outputLocation, "w") as f:
	for venue in sorted(trainingData.indicesByCanonicalVenue):
		f.write(venue + "\n")