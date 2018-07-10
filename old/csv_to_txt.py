#!/usr/bin/env python

import sys
import helper
import csv

if len(sys.argv) < 3:
    print("Usage: {} IN.csv OUT_FOLDER".format(sys.argv[0]))
    exit(1)

filename = sys.argv[1]
out_folder = sys.argv[2]

topic_notes = helper.getNotesFromCSV(filename)

duplicates_found = False
for topic, notes in topic_notes.iteritems():
    duplicates = helper.getDuplicates(notes)
    if len(duplicates) > 0:
        duplicates_found = True
        print "Found duplicate in topic '{}':\t'{}'".format(topic, duplicates)

if duplicates_found is True:
    print "Duplicates found - exiting!"
    exit(1)

for topic, notes in topic_notes.iteritems():
    with open("{}/{}.txt".format(out_folder, topic), 'w') as file:
        fieldnames = ['title', 'content']
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        for note in notes:
            writer.writerow(note)
