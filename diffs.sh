#!/usr/bin/env sh

set -x

CSV_FILE=$1

if [[ -z $CSV_FILE ]]; then
    CSV_FILE=../anki_export.csv
fi

TMP_DIR=`mktemp -d`
./csv_to_txt.py ${CSV_FILE} ${TMP_DIR} || exit 1
git diff ${TMP_DIR} data