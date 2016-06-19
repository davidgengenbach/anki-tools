#!/usr/bin/env python

import json
import sys
import os

if len(sys.argv) < 2:
    print "Usage: {} file1.json file2.json".format(sys.argv[0])
    exit(1)

files = sys.argv[1:]
files_names = map(lambda x : {"json": x, "name": os.path.splitext(x)[0]}, files)

result = []
for file in files_names:
    if file["name"] == "notes":
        continue
    with open(file["json"], 'r') as content_file:
        content = json.load(content_file)
    result.append({
        "name": file["name"],
        "notes": content
    })

with open('notes.json', 'w') as file:
    json.dump(result, file)