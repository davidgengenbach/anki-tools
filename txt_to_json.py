#!/usr/bin/env python

# TODO

import re
import sys
import json
import os

if len(sys.argv) < 2:
    print("Usage: {} filename".format(sys.argv[0]))
    exit(1)

seperator = ("-" * 100);
filename = sys.argv[1]
p = re.compile('"(.*)","(.*)"')

def get_all_notes(filename):
    count = 0;
    elements = []
    errors = []
    with open(filename, 'r') as file:
        for line in file:
            count = count + 1
            matched = p.search(line)
            if not matched:
                errors.append({"lineNr": count, "line": line})
                continue
            title = matched.group(1)
            content = matched.group(2)
            elements.append({'title': title, 'content': content})
    return (elements, errors)

(elements, errors) = get_all_notes(filename)

if len(errors) is not 0:
    for error in errors:
        print "Error in Line {}: {}".format(error["lineNr"], error["line"])
    with open(os.path.splitext(filename)[0] + '_errors.json', 'w') as file:
        json.dump(errors, file);

with open(os.path.splitext(filename)[0] + '.json', 'w') as file:
    json.dump(elements, file);


