#!/usr/bin/env sh


usage() {
    echo "$0 FILE_TO_COMPARE.txt CSV_FILE.csv"
}

FILE_TO_COMPARE=$1
CSV_FILE=$2

if [[ -z $CSV_FILE ]]; then
    CSV_FILE=../anki_export.csv
fi

if [[ -z $FILE_TO_COMPARE ]]; then
    FILE_TO_COMPARE='data/CER.txt'
fi

filename=$(basename "$FILE_TO_COMPARE")
extension="${filename##*.}"
filename="${filename%.*}"

TMP_DIR=`mktemp -d`
./csv_to_txt.py ${CSV_FILE} ${TMP_DIR} || exit 1
./compare_txts.py ${TMP_DIR}/${filename}.${extension} $FILE_TO_COMPARE
