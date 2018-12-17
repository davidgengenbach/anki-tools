#!/usr/bin/env bash

./1_import_anki_csv.py
./2_convert_csvs_to_txt.py
./s_export_to_csv.sh

./diff.sh
