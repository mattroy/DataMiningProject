DataMiningProject
=================
Project for cs6220

###Steps for generating new predictions.
1. Add the training file to the data directory as "AP_train.txt"
2. Add the new test file to the data directory as "AP\_test\_par.txt"
3. Run `./MineDataSet.sh` from the main directory.

###Steps for Old Baseline
1. Copy the ap_train.txt file to the data directory.
2. Make sure you have python and numpy installed.
2. Edit the config file if you have renamed any files or directories.
3. Run the split_data script, this will create a validation set and a ground truth file.
4. Run the baseline script, this will create a baseline set of predictions for the validation set.
5. Run the score_results script this will calculate the score of the baseline script on the validation set.

###Directories
* data
* output
* scripts
* test

####data
The test file is checked in here. The training data is not checked in due to size issues. You will need to add your copy of ap_train.txt here.

####output
The output of scripts will be put here.

####scripts
Scripts to be run on data here.

* split_data.py - this script splits the data into a validation and training set. This works by getting 10 percent of the papers from 2012 for the validation set. The rest of the data is put in the training set.
* baseline.py - this script is a basic baseline predictor...
* score_results - evaluate the ground truth and the predictions based on the MAPK function the eval will use.
* papers.py - class for paper, which holds data about a single paper. Class for corpus which holds a large set of papers and allows for retrieval in a few different ways.
* papers_test.py - unit tests for the papers class.
* mapk.py - this was taken from Ben Horners implementation of the MAPK function from Kaggle. It is used in the scoring script.
* feature_gen.py - creates feature file for training svm. Output is in format for libsvm.
* stop_words.txt - a list of stopwords to be removed from paper titles and abstracts when processing.
* get_venues.py - list all the canonical venues found in a corpus. This is useful for seeing if papers have the same venue, but a slight naming difference causes them to be in different venues.
* get\_paper\_refs.py - list the number of refs per paper for the training set.
* eval_features.py - creates a feature file for papers in the eval data set.
* parse_prediction.py - generate the results file from the svm-prediction file and the map file.

---
* svm_config - final config for running the svm scripts.
* config.cfg - contains settings for all scripts, this will be useful to run multiple experiments without needing to edit the code or move/edit the existing ouputs
* config2.cfg - a config file for the evaluation set
* test.cfg - this specifies some test data instead of evaluation data.

####tests
Files for testing.

* feature_tests.txt - used for testing the feature generation code
* test_corpus.txt - used for unit tests
