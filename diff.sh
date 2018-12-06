#!/usr/bin/env bash

current=../anki
last_backup=$(ls ../anki_backup | sort -n | tail -n1)

diff --minimal --color --exclude='*.csv' ../anki_backup/$last_backup $current
