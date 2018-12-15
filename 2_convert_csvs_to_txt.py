#!/usr/bin/env python3

import helper
from glob import glob
import os


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Converts CSV files to txt')
    parser.add_argument('--csv_folder', type=str, default='../anki/csv')
    parser.add_argument('--txt_folder', type=str, default='../anki')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    files = glob(os.path.join(args.csv_folder, '*.csv'))
    for file in files:
        new_file = os.path.join(args.txt_folder, helper.get_filename(file, False) + '.anki.txt')
        rows = helper.get_csv(file)
        lines = [helper.csv_line_to_txt(x) for x in rows]
        helper.write_file(new_file, '\n\n'.join(lines))


def join(x, delimiter='//'):
    return delimiter.join(x).strip()


if __name__ == '__main__':
    main()
