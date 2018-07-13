#!/usr/bin/env bash

while inotifywait -e close_write ../anki/*.txt; do
	./s_export.sh;
done