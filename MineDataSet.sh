
#!/bin/bash
set -e


#1. run the gen_features script
echo "run the gen_features script"
python


#2. run eval_features
#3. run svm-predict
#4. run svm-train
#5. run svm-predict2:03 AM
#6. run Saoni's new script


#get the branch name and also the locale
basebranch=$1
comparebranch=$2
locale=$3
affiliate=$4

#create the name of the new branch dir for diff images example : diff-R198a
diffName="diff-"
diffName+="$basebranch"

set completion-ignore-case On affiliate

#get the affiliate dir
if [ "$affiliate" == "kayak" ] || [ "$affiliate" == "KAYAK" ] || [ "$affiliate" == "Kayak" ]
then
    affiliate="locale"
else
    locale="$affiliate$locale"
    affiliate="affiliate"
fi

#check for locale which can be none
if [ "$locale" != "none" ]
then

#the address where the diff images are located
mydir=./wraith-output
prevdir="/home/bamboo/screenshots/quickProdTest/${comparebranch}/prod/archive/${affiliate}/${locale}/"
newmydir="/home/bamboo/screenshots/quickProdTest/${comparebranch}/prod/archive/${affiliate}/${locale}/${diffName}/"
files="./wraith-output/*"

#give permission to create the dir for diff images and crate a diff dir
chmod -R 777 $prevdir
mkdir -p $prevdir/$diffName


#name of the diff image
FILENAME="600_phantomjs_Rdiff"
#the length of png-directory
EXTENTIONLENGTH=14

#going through each dir
for f in $files
do
 if [ -d "$f" ]
    dirname=$(basename "$f")
    dirLength="${#dirname}"
 then
        for ff in $f/*
            do
                filename=$(basename "$ff")
                extension="${filename##*.}"
                filename="${filename%.*}"
                if [ "$filename" = "$FILENAME" ]
                    then
                        let "dirLength -= 14"
                        newFileName=${dirname:0:dirLength}
                        newFileName+="-diff.png"
                        cp $ff $newmydir/$newFileName
                fi
        done
 fi
done
fi