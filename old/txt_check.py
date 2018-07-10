#!/usr/bin/env python


import helper, sys

if len(sys.argv) < 2:
    print "Usage: {} file1.txt".format(sys.argv[0])
    exit(1)

files = sys.argv[1:]
files_names = map(lambda x : {"txt": x, "name": helper.getFilename(x)['filenameWithoutExtension']}, files)

errorFound = False
for file in files_names:
    (notes, errors) = helper.getNotesFromTxt(file['txt'])
    for error in errors:
        errorFound = True
        print "Error ({}:{}): '{}'".format(file['txt'], error['lineNr'], error['line'])

exit(1 if errorFound else 0)