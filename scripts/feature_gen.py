#feature_gen.py
#
#This script creates a feature file for training.
#
#Data Mining Project
#CS6220 Fall 2014
#Team ELSAMAT

import sys
import os
import ConfigParser
import papers
import random

config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

trainingLocation = config.get('split_data', 'training_location')
featureLocation = config.get('prediction', 'feature_location')

print "----------------------------------------------------------------------------"
print "- Load config from:          ", sys.argv[1]
print "- Load training data from:   ", trainingLocation

print "- Feature output at:     ", featureLocation
print "----------------------------------------------------------------------------"

trainingData = papers.Corpus()
trainingData.readCorpus(trainingLocation)

print "- Loaded training file with: ", len(trainingData.papersByRef), " papers in it."
print "----------------------------------------------------------------------------"
with open(featureLocation, "w", 0) as file:
	for paperId in trainingData.papersByRef:
		currentPaper = trainingData.papersByRef[paperId]
		
		queue = []
		
		queue.extend(currentPaper.references)
		
		for i in range(50):
			queue.append(random.choice(trainingData.papersByRef.keys()))
		
		print "Queue length for paper: ", paperId, " is ", len(queue)
		for comparisonId in queue:

			if nextPaperId not in trainingData.papersByRef:
                continue

			comparisonPaper = trainingData.papersByRef[comparisonId]
			
			if comparisonId == paperId: 
				continue
			
			if comparisonPaper.year > currentPaper.year:
				continue	
			
			#label
			if comparisonId in currentPaper.references:
				file.write("1 ")
			else:
				file.write("0 ")
				
			#feature 1: chances of reference
			if currentPaper.canonicalVenue in trainingData.venueReferences:
				if comparisonPaper.canonicalVenue in trainingData.venueReferences[currentPaper.canonicalVenue]:
					percent = trainingData.venueReferences[currentPaper.canonicalVenue][comparisonPaper.canonicalVenue] / float(trainingData.venueReferenceCount[currentPaper.canonicalVenue])
					file.write("1:" + str(percent) + " ")
				else:
					file.write("1:0 ")
			else: 
				file.write("1:0 ")
				
			#feature 2: title similarity
			file.write("2:" + str(currentPaper.titleCosineSimilarity(comparisonPaper.titleList)) + " ")
			
			#feature 3: abstract similarity
			file.write("3:" + str(currentPaper.abstractCosineSimilarity(comparisonPaper.abstractList)) + " ")
			
			#feature 4: years since publish
			file.write("4:" + str(currentPaper.year - comparisonPaper.year) + "\n")

            #feature 4: years since publish
            file.write("5:" + str(currentPaper.author + "\n")


