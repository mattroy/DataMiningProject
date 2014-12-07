
#!/bin/bash
set -e


#1. run the gen_features script
echo "run the features generator script"
python ./scripts/feature_gen.py svm_config
echo "-----------------FINISHED FEATURE GENERATOR--------------------------"
echo


#2. run eval_features
echo "run the eval features script"
python ./scripts/eval_features.py
echo "-----------------FINISHED EVAL FEATURE--------------------------"
echo


#3. run svm-train
echo "run the svm-train"
./libsvm/svm-train
echo "-----------------FINISHED SVM train--------------------------"
echo


#4. run svm-predict
echo "run the svm-predict"
./libsvm/svm-predict
echo "-----------------FINISHED SVM predict--------------------------"
echo


#5. run Saoni's new script
echo "run the parseMap"
python ./scripts/parse_prediction.py svm_config
echo "-----------------FINISHED ParseMap--------------------------"
echo
