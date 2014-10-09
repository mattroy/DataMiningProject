#split_data.py
#
#The purpose of this script is to split the training data into a test and validation set.

import sys
import os
import ConfigParser
import random

config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

validationSize = config.get('split_data', 'validation_size')
trainingData = config.get('split_data', 'training_location')
outputLocation = config.get('split_data', 'output_location')
trainingLocation = config.get('split_data', 'training_output_location')
validationLocation = config.get('split_data', 'validation_location')

print "-----------------------------------"
print "Load config from:                ", sys.argv[1]
print "Training data will be split into ", validationSize, "% validation and ", 100 - int(validationSize), "% training"
print "Trainingg data is at             ", trainingData
print "Output is at                     ", outputLocation
print "-----------------------------------"

if not os.path.exists(outputLocation):
    os.makedirs(outputLocation) 

validationFile = open(os.path.join(outputLocation,validationLocation) , "w")
trainingFile = open(os.path.join(outputLocation, trainingLocation), "w")

sample = ""
validationCount = 0
trainingCount = 0
with open(trainingData) as f:
    for line in f:
        if line.startswith("#index"):
            if(random.randint(0,100) <= int(validationSize)):
                validationFile.write(sample)
                validationCount += 1
            else:
                trainingFile.write(sample)
                trainingCount += 1
            sample = line
        else:
            sample += line

print "Created ", validationCount, " validation samples"
print "Created ", trainingCount, " training samples"
print "At ", float(validationCount)/float(trainingCount) * 100, "% of validation files"