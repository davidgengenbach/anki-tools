#!/usr/bin/env python3

import io
import csv
from helper import to_csv, write_csv
from enum import Enum
import sys

class ParserModes(Enum):
    FRONT = 'front'
    BACK = 'back'

def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Convert text file of notes to CSV')
    parser.add_argument('--in_file', type=str, default='../anki/data.txt')
    parser.add_argument('--write_csv', action='store_true')
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    rows = get_parsed_notes(args.in_file)
    csv = to_csv(rows)
    if args.write_csv:
        write_csv(args.in_file + '.csv', rows)
    print(csv)
    sys.stderr.write('\n\n!\tDo not forget to execute ./3_convert_csv.py\t!\n\n\n')

def get_parsed_notes(file):
    with open(file) as f:
        return parse_text(f.readlines())

def parse_text(lines, front_delimiter='((', back_delimiter='))'):
    all_lines = []
    mode = None
    current = None
    for line in lines:
        line = line.strip()
        if line.startswith(front_delimiter):
            if current is not None:
                all_lines.append(current)
            current = {ParserModes.FRONT: [], ParserModes.BACK: []}
            mode = ParserModes.FRONT
        elif line.startswith(back_delimiter):
            mode = ParserModes.BACK
        assert mode is not None
        line = clean_line(line, [front_delimiter, back_delimiter])
        if line != '':
            current[mode].append(line)
    if current is not None:
        all_lines.append(current)
    return [(join(line[ParserModes.FRONT]), join(line[ParserModes.BACK])) for line in all_lines]

def clean_line(x, remove_chars=[]):
    for y in remove_chars:
        x = x.replace(y, '')
    return x.strip()

def join(x, delimiter='//'):
    return delimiter.join(x).strip() 

if __name__ == '__main__':
    main()
