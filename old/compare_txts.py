#!/usr/bin/env python

import sys
import helper
from pprint import pprint

if len(sys.argv) < 3:
    print "Usage: {} file1.txt file2.txt".format(sys.argv[0])
    exit(1)

file1 = sys.argv[1]
file2 = sys.argv[2]

(notes1, errors1) = helper.getNotesFromTxt(file1)
(notes2, errors2) = helper.getNotesFromTxt(file2)

def diff(a, b):
    return [aa for aa in a if aa not in b]

sort_fn = lambda x: x['title']
notes1 = sorted(notes1, key = sort_fn)
notes2 = sorted(notes2, key = sort_fn)

def find_by_attribute(l, attr, val):
    for i in l:
        if i[attr] == val:
            return i
    return None

for diff_e in diff(notes1, notes2):
    title = diff_e['title']
    a = find_by_attribute(notes1, 'title', title)
    b = find_by_attribute(notes2, 'title', title)
    if a is None or b is None:
        print('Title: {}\nOnly in {}'.format(title, 'NEW' if a is None else 'REFERENCE'))
    else:
        print 'Title: {}\nFIRST:\t"{}"\nSECOND:\t"{}"'.format(title, a['content'], b['content'])
    print '\n'

