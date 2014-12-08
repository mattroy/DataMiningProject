#!/bin/bash
set -e

#1. run eval_features
echo "run the eval features script"
python ./scripts/eval_features.py svm_config
echo "-----------------FINISHED EVAL FEATURE--------------------------"
echo

echo "make lib-svm"
./libsvm-3.20/make
echo "----------------MADE LIB SVM------------------------------------"


#2. run svm-predict
echo "run the svm-predict"
./libsvm/svm-predict 
echo "-----------------FINISHED SVM predict--------------------------"
echo


#3. Parse the svm results and generate a prediction file
echo "run the parsing"
python ./scripts/parse_prediction.py svm_config
echo "-----------------FINISHED ParseMap-----------------------------"
echo
