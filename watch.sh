#!/usr/bin/env bash

./s_export.sh

while inotifywait --quiet --event close_write ../anki/*.txt; do
  echo '#####################################################'
	./s_export.sh
done