#score_results.py
#
#The purpose of this script is to score the results of a validation.
#
#It takes as input a GT file and a result file.
#
#Data Mining Project
#CS6220 Fall 2014
#Team ELSAMAT

import ConfigParser
import mapk
import numpy as np
import os
import sys

config = ConfigParser.ConfigParser()
config.read(sys.argv[1])

outputLocation = config.get('score_results', 'output_location')
gtLocation = config.get('score_results', 'gt_file')
resultsLocation = config.get('score_results', 'result_file')
maxPredictions = config.get('score_results', 'max_num_predictions')


print "----------------------------------------------------------------------------"
print "- Load config from:     ", sys.argv[1]
print "- Ground truth file is  ", gtLocation
print "- Results file is       ", resultsLocation
print "- Number of predictions ", maxPredictions
print "----------------------------------------------------------------------------"

gtDic = {}
resultDic = {}

with  open(os.path.join(outputLocation,gtLocation) , "r") as gtFile:
    for line in gtFile:
        splitLine = line.split(',')
        gtDic[splitLine[0]] = splitLine[1][1:-1].split(" ")

with  open(os.path.join(outputLocation,resultsLocation) , "r") as resultFile:
    for line in resultFile:
        splitLine = line.split(',')
        resultDic[splitLine[0]] = splitLine[1][1:-1].split(" ")


gtList = []
resultList = []
for paper in gtDic:
    gtList.append(gtDic[paper])

    if paper in resultDic:
        resultList.append(resultDic[paper])
    else:
        resultList.append([])

score = mapk.apk(gtList, resultList, maxPredictions)

print "- Score of predictions: ", score 
print "----------------------------------------------------------------------------"
