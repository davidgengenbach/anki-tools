#!/usr/bin/env python

import re
import sys
import json
import os
import helper

if len(sys.argv) < 3:
    print "Usage: {} OUT.json file1.txt file2.txt".format(sys.argv[0])
    exit(1)

out = sys.argv[1]
files = sys.argv[2:]
files_names = map(lambda x : {"txt": x, "name": helper.getFilename(x)['filenameWithoutExtension']}, files)

result = []
for file in files_names:
    if file["name"] == "notes":
        continue
    (notes, errors) = helper.getNotesFromTxt(file['txt'])
    result.append({
        "name": file["name"],
        "notes": notes
    })

with open(out, 'w') as out_file:
    json.dump(result, out_file)