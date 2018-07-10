#!/usr/bin/env python3

from collections import defaultdict
from helper import get_csv, write_csv, backup_folder, linebreak_to_txt
import os
import sqlite3
import json
import csv
import os
import numpy as np

def get_args():
    import argparse
    default_db_path = os.path.join(os.path.expanduser("~"), '.local/share/Anki2/User 1/collection.anki2')
    parser = argparse.ArgumentParser(description='Import Anki cards from sqlite3 database')
    parser.add_argument('--db_path', type=str, default=default_db_path)
    parser.add_argument('--out_folder', type=str, default='../anki')
    parser.add_argument('--backup_folder', type=str, default='../anki_backup')
    args = parser.parse_args()
    return args

def main():
    args = get_args()

    if not np.all([os.path.exists(x) for x in [args.db_path, args.out_folder, args.backup_folder]]):
        print('Invalid paths!')
        sys.exit(1)

    conn = sqlite3.connect(args.db_path)
    rows = get_cards(conn)

    header = rows[0]
    rows = rows[1:]

    if not rows_valid(rows):
        print('ABORTING')
        sys.exit(1)
   
    backup_folder(args.out_folder, backup_folder = args.backup_folder)

    cards_per_deck = defaultdict(list)
    for front, back, deck in rows:
        cards_per_deck[deck].append((front, back))

    for deck, cards in cards_per_deck.items():
        filename = os.path.join(args.out_folder, '{}.csv'.format(deck))
        write_csv(filename, [(linebreak_to_txt(front), linebreak_to_txt(back)) for front, back in cards])

def get_cards(conn):
    id_2_name = get_deck_id_2_deck_name(conn)
    cards = []
    for id_, flds in get_notes(conn):
        front, back = split_field(flds)
        front, back = linebreak_to_txt(front), linebreak_to_txt(back)
        did = get_deck_id_from_card(conn, id_)
        assert(did is not None)
        assert(did in id_2_name.keys())
        deck = id_2_name[did]
        cards.append((front, back, deck))

    for row in cards: assert(len(row) == 3)

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
    return conn.cursor().execute('SELECT id, flds FROM notes')

def get_deck_id_from_card(conn, id_):
    return conn.cursor().execute('SELECT did FROM cards WHERE nid = ' + str(id_)).fetchone()[0]

def split_field(x):
    return x.split("\x1f")

if __name__ == '__main__':
    main()