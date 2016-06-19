#!/usr/bin/env python

import sys
import helper

if len(sys.argv) < 3:
    print("Usage: {} IN.csv OUT_FOLDER".format(sys.argv[0]))
    exit(1)

filename = sys.argv[1]
out_folder = sys.argv[2]

elements = helper.getNotesFromCSV(filename)

for topic, notes in elements.iteritems():
    with open("{}/{}.txt".format(out_folder, topic), 'w') as file:
        for note in notes:
            file.write('"{}","{}"\n'.format(note['title'], note['content']))
