#baseline.py
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

trainingLocation = config.get('prediction', 'training_location')
validationLocation = config.get('prediction', 'validation_location')
predictionLocation = config.get('prediction', 'prediction_location')


print "----------------------------------------------------------------------------"
print "- Load config from:          ", sys.argv[1]
print "- Load training data from:   ", trainingLocation
print "- Load validation data from: ", validationLocation
print "- Predciction output at:     ", predictionLocation
print "----------------------------------------------------------------------------"

trainingData = papers.Corpus()
trainingData.readCorpus(trainingLocation)

validationData = papers.Corpus()
validationData.readCorpus(validationLocation)

#heurisitic based prediction
predictions = []
for paper in validationData.papersByRef:
	currentPaper = validationData.papersByRef[paper]
	refs = []
	for otherPaper in trainingData.papersByRef:
		nextPaper = trainingData.papersByRef[otherPaper]
		if(nextPaper.year < currentPaper.year and nextPaper.index != currentPaper.index):
			sim = currentPaper.abstractCosineSimilarity(nextPaper.abstract)
			refs = papers.appendMax((nextPaper.index, sim), refs, 10)

	print "Add prediction for paper: ", paper
	predictions.append((paper, [x[0] for x in refs]))


	# refs = []
	# authors = validationData.papersByRef[paper].authors
	# for author in authors:
	# 	if author in validationData.indicesByAuthor:
	# 		refs += validationData.indicesByAuthor[author]
	# for author in authors:
	# 	if author in trainingData.indicesByAuthor:
	# 		refs += trainingData.indicesByAuthor[author]
	# predictions.append((paper, refs)) 

with open(predictionLocation, "w") as file:
	file.write("index, references\n")
	for entry in predictions:
		reference, refs = entry
		file.write(reference + ", " + " ".join(refs) + "\n")

print "- Number of training papers:   ", len(trainingData.papersByRef)
print "- Number of validation papers: ", len(validationData.papersByRef)
print "----------------------------------------------------------------------------"
