#!/usr/bin/env sh

txt_files=`find data -type f -name *.txt`
./txt_check.py $txt_files