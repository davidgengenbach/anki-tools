#!/usr/bin/env python3

from collections import defaultdict
from helper import write_csv, backup_folder, linebreak_to_txt, get_default_db_path
import sqlite3
import json
import os
import numpy as np
import sys


def get_args():
    import argparse
    parser = argparse.ArgumentParser(description='Import Anki cards from sqlite3 database')
    parser.add_argument('--db_path', type=str, default=get_default_db_path())
    parser.add_argument('--backup_folder_src', type=str, default='../anki')
    parser.add_argument('--csv_folder', type=str, default='../anki/csv')
    parser.add_argument('--backup_folder', type=str, default='../anki_backup')
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    if not np.all([os.path.exists(x) for x in [args.db_path, args.csv_folder, args.backup_folder]]):
        print('Invalid paths!')
        sys.exit(1)

    conn = sqlite3.connect(args.db_path)

    rows = get_cards(conn)
    header, rows = rows[0], rows[1:]

    if not rows_valid(rows):
        sys.stderr.write('ABORTING\n')
        sys.exit(1)

    backup_folder(args.backup_folder_src, backup_folder=args.backup_folder)

    cards_per_deck = defaultdict(list)
    for front, back, deck in rows:
        cards_per_deck[deck].append((front, back))

    for deck, cards in cards_per_deck.items():
        filename = os.path.join(args.csv_folder, '{}.csv'.format(deck))
        write_csv(filename, rows)


def get_cards(conn):
    id_2_name = get_deck_id_2_deck_name(conn)
    cards = []

    for did, id_, flds in get_notes(conn):
        front, back = [linebreak_to_txt(x) for x in split_field(flds)]
        assert (did is not None)
        assert (did in id_2_name.keys())
        deck = id_2_name[did]
        cards.append((front, back, deck))

    for row in cards: assert (len(row) == 3)

    return [('Front', 'Back', 'Deck')] + cards


def rows_valid(rows):
    valid = True
    for line_no, row in enumerate(rows):
        if len(row) != 3:
            print('Line: {}: wrong number of fields = {}'.format(line_no + 1, len(row)))
            valid = False
    return valid


def get_deck_id_2_deck_name(conn):
    id_2_name = dict()
    for row in conn.cursor().execute('SELECT decks FROM col'):
        for did, desc in json.loads(row[0]).items():
            name = desc['name']
            id_2_name[int(did)] = name
    return id_2_name


def get_notes(conn):
    return conn.cursor().execute('''
      SELECT cards.did, notes.id, notes.flds
      FROM notes
      INNER JOIN cards on cards.nid = notes.id
    '''.strip())


def split_field(x):
    return x.split("\x1f")


if __name__ == '__main__':
    main()
