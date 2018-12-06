#!/usr/bin/env python3

import helper
from helper import to_csv, write_csv
from enum import Enum
from glob import glob
import os


class ParserModes(Enum):
    FRONT = 'front'
    BACK = 'back'


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Convert text file of notes to CSV')
    parser.add_argument('--txt_folder', type=str, default='../anki')
    parser.add_argument('--csv_folder', type=str, default='../anki/csv')
    parser.add_argument('--write_csv', action='store_true')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    txt_files = glob(os.path.join(args.txt_folder, '*.txt'))
    for file in txt_files:
        convert_txt_to_csv(file, args.csv_folder, args.write_csv)


def convert_txt_to_csv(file, csv_folder, save_to_csv=False):
    rows = get_parsed_notes(file)
    csv = to_csv(rows)
    if save_to_csv:
        filename = helper.get_filename(file, with_extension=False) + '.csv'
        write_csv(os.path.join(csv_folder, filename), rows)
    return csv


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
        line = helper.replace(line, [front_delimiter, back_delimiter])
        if line == front_delimiter or line == back_delimiter:
            continue
        current[mode].append(line.strip())
    
    if current is not None:
        all_lines.append(current)

    return [(helper.txt_lines_to_csv(line[ParserModes.FRONT]), helper.txt_lines_to_csv(line[ParserModes.BACK])) for line in all_lines]


if __name__ == '__main__':
    main()
