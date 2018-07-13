#!/usr/bin/env python3

from glob import glob
import os
from helper import get_csv, write_csv, linebreak_to_html, get_filename, remove_file


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Cleans and converts CSV (removes line-breaks, ...)')
    parser.add_argument('--csv_folder', type=str, default='../anki/csv')
    parser.add_argument('--csv_converted_folder', type=str, default='../anki/converted')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    os.makedirs(args.csv_converted_folder, exist_ok=True)
    files = glob(os.path.join(args.csv_folder, '*.csv'))
    for file in files:
        name = get_filename(file, with_extension=False)
        print(name)
        new_filename = os.path.join(args.csv_converted_folder, name + '.csv')
        lines = get_csv(file)
        if not rows_are_valid(lines):
            print('\t (Skipping)')
            remove_file(new_filename)
            continue
        converted_lines = list(map(convert_line, lines))
        write_csv(new_filename, converted_lines)
        print()


def rows_are_valid(rows):
    valid = True
    for idx, line in enumerate(rows):
        for field in line:
            if field.count('IMAGE') != 0:
                print('\t Line: {}: IMAGE'.format(idx + 1))
            if field.count('\n') != 0:
                valid = False
                print('\t Line {}: has line-break'.format(idx + 1))
            if 'TDB' in field or 'TBD' in field or '???' in field:
                print('\t Line {:4}: TBD ("{}")'.format(idx + 1, line[0]))
        if len(line) != 2:
            valid = False
            print('\t Line {}: wrong field count {}'.format(idx + 1, len(line), line))
    return valid


def convert_line(line):
    return [linebreak_to_html(x) for x in line]


if __name__ == '__main__':
    main()
