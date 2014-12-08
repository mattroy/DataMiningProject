#eval_features.py
#
#This script creates a feature file for predicting the references of the 
#evaluation data.
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

trainingDataLocation = config.get('prediction', 'training_location')
evalDataLocation = config.get('prediction', 'eval_data')
featureLocation = config.get('prediction', 'eval_feature_location')
featureMapLocation = config.get('prediction', 'feature_map_location')


print "----------------------------------------------------------------------------"
print "- Load config from:          ", sys.argv[1]
print "- Load training data from: ", trainingDataLocation
print "- Load eval data from:   ", evalDataLocation

print "- Feature output at:     ", featureLocation
print "----------------------------------------------------------------------------"

trainingData = papers.Corpus()
trainingData.readCorpus(trainingDataLocation)

evalData = papers.Corpus()
evalData.readCorpus(evalDataLocation)

print "- Loaded training file with: ", len(trainingData.papersByRef), " papers in it."
print "----------------------------------------------------------------------------"
mapFile = open(featureMapLocation, "w", 0)

with open(featureLocation, "w", 0) as file:
    for paperId in evalData.papersByRef:
        currentPaper = evalData.papersByRef[paperId]

        if currentPaper.canonicalVenue in trainingData.venueReferences:
            print "For paper: ", paperId, " there are ", len(trainingData.venueReferences[currentPaper.canonicalVenue]), " venues"
            
            for venue in trainingData.venueReferences[currentPaper.canonicalVenue]:
                for comparisonId in trainingData.indicesByCanonicalVenue[venue]:

                    if comparisonId not in trainingData.papersByRef:
                        continue

                    comparisonPaper = trainingData.papersByRef[comparisonId]
                    
                    percent = 0
                    if currentPaper.canonicalVenue in trainingData.venueReferences:
                        if comparisonPaper.canonicalVenue in trainingData.venueReferences[currentPaper.canonicalVenue]:
                            percent = trainingData.venueReferences[currentPaper.canonicalVenue][comparisonPaper.canonicalVenue] / float(trainingData.venueReferenceCount[currentPaper.canonicalVenue])

                    if percent < 0.01:
                        continue

                    if comparisonId == paperId: 
                        continue
                
                    if comparisonPaper.year > currentPaper.year:
                        continue    

                    #Map file holds a list of the comparisions for lookup after the prediction step
                    mapFile.write(paperId + ":" + comparisonId + "\n")
                    
                    #label
                    if comparisonId in currentPaper.references:
                        file.write("1 ")
                    else:
                        file.write("0 ")
                        
                    #feature 1: chances of reference
                    file.write("1:" + str(percent) + " ")
                        
                    #feature 2: title similarity
                    file.write("2:" + str(currentPaper.titleCosineSimilarity(comparisonPaper.titleList)) + " ")
                    
                    #feature 3: abstract similarity
                    file.write("3:" + str(currentPaper.abstractCosineSimilarity(comparisonPaper.abstractList)) + " ")
                    
                    #feature 4: years since publish
                    file.write("4:" + str(currentPaper.year - comparisonPaper.year) + " ")

                    #feature 5: authors similarity
                    file.write("5:" + str(currentPaper.authorsCosineSimilarity(comparisonPaper.authors)) + " ")

                    #feature 6: number of times the comparison paper has been referenced.
                    if comparisonId in trainingData.paperReferenceCount:
                        file.write("6:" + str(trainingData.paperReferenceCount[comparisonId]) + "\n")
                    else:  
                        file.write("6:" + "0\n")
       