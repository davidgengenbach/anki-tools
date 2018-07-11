#!/usr/bin/env python3

import helper
from glob import glob
import os


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Converts CSV files to txt')
    parser.add_argument('--csv_folder', type=str, default='../anki/csv')
    parser.add_argument('--out_folder', type=str, default='../anki')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    files = glob(os.path.join(args.csv_folder, '*.csv'))
    for file in files:
        new_file = os.path.join(args.out_folder, helper.get_filename(file, False) + '.txt')
        rows = helper.get_csv(file)
        lines = [convert_card_to_txt(x) for x in rows]
        helper.write_file(new_file, '\n\n'.join(lines))


def convert_card_to_txt(row):
    row = [helper.linebreak_to_real(x) for x in row]
    return '((\n{}\n))\n{}\n'.format(*row)


def join(x, delimiter='//'):
    return delimiter.join(x).strip()


if __name__ == '__main__':
    main()