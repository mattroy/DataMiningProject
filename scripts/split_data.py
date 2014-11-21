#split_data.py
#
#The purpose of this script is to split the training data into a test and validation set.
#It will remove, articles with less than 10 references
#It also creates a ground truth file for the validation set.
#
#Data Mining Project
#CS6220 Fall 2014
#Team ELSAMAT

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
gtLocation = config.get('split_data', 'gt_location')

print "----------------------------------------------------------------------------"
print "- Load config from:                ", sys.argv[1]
print "- Training data will be split into ", validationSize, "% validation and ", 100 - int(validationSize), "% training"
print "- Trainingg data is at             ", trainingData
print "- Output is at                     ", outputLocation
print "----------------------------------------------------------------------------"

if not os.path.exists(outputLocation):
    os.makedirs(outputLocation) 

validationFile = open(os.path.join(outputLocation,validationLocation) , "w")
trainingFile = open(os.path.join(outputLocation, trainingLocation), "w")
gtFile = open(os.path.join(outputLocation, gtLocation), "w")
gtFile.write("Id,References\n")

sample = ""
validationGTLine = ""
gtCount = 0
badDataCount = 0
validationCount = 0
trainingCount = 0
sampleYear = 0
with open(trainingData) as f:
    for line in f:
        if line.startswith("#index"):
            if sampleYear == 2012:
                if(random.randint(1,100) < int(validationSize)):
                    validationFile.write(sample)
                    validationCount += 1
                    gtFile.write(validationGTLine + "\n")
            else:
                trainingFile.write(sample)
                trainingCount += 1
                
            gtCount = 0
            sample = line
            validationGTLine = line[7:-1] + ","

        elif line.startswith("#%"):
            if gtCount < 10:
                validationGTLine += " " + line[3:-1]
                gtCount += 1    
            sample += line

        elif line.startswith("#t"):
            sampleYear = line[3:].strip()
            sample += line
            
        else:
            sample += line

print "- Removed ", badDataCount, " lines."
print "- Created ", validationCount, " validation samples"
print "- Created ", trainingCount, " training samples"
print "- At ", float(validationCount)/float(trainingCount) * 100, "% of validation files"
print "----------------------------------------------------------------------------"