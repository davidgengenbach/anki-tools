#!/usr/bin/env bash

./s_export_to_csv.sh

while inotifywait --quiet --event close_write ../anki/*.txt; do
  echo '#####################################################'
	./s_export_to_csv.sh
done