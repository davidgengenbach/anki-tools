#!/usr/bin/env python

import json
import sys
import helper

if len(sys.argv) < 3:
    print("Usage: {} IN OUT".format(sys.argv[0]))
    exit(1)

filename = sys.argv[1]
out_filename = sys.argv[2]

with open(out_filename, 'w') as file:
    json.dump(helper.getNotesFromCSV(filename), file)
