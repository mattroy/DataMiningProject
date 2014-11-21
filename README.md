DataMiningProject
=================
Project for cs6220

###Steps
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
* mapk.py - this was taken from Ben Horners implementation of the MAPK function from Kaggle. It is used in the scoring script.
* config.cfg - contains settings for all scripts, this will be useful to run multiple experiments without needing to edit the code or move/edit the existing ouputs

####tests
Files for testing.

* papers_test - unit tests for the papers class