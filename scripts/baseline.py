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
with open(predictionLocation, "w", 0) as file:
	file.write("Id,References\n")
	for paper in validationData.papersByRef:
		currentPaper = validationData.papersByRef[paper]
		refs = []
		if currentPaper.venue in trainingData.indicesByVenue:
			print "For paper: ", paper, " there are ", len(trainingData.indicesByVenue[currentPaper.venue])
			for nextPaperId in trainingData.indicesByVenue[currentPaper.venue]:
				nextPaper = trainingData.papersByRef[nextPaperId]
				if(nextPaper.year < currentPaper.year and nextPaper.index != currentPaper.index):
					sim = currentPaper.abstractCosineSimilarity(nextPaper.abstract)
					refs = papers.appendMax((nextPaper.index, sim), refs, 10)
			prediction = [x[0] for x in refs]
			# predictions.append((paper, ))
		else:
			prediction = []
			# predictions.append((paper, []))
		file.write(paper + ", " + " ".join(prediction) + "\n")




	
	# for entry in predictions:
	# 	reference, refs = entry
		
print "- Number of training papers:   ", len(trainingData.papersByRef)
print "- Number of validation papers: ", len(validationData.papersByRef)
print "----------------------------------------------------------------------------"
