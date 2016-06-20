import csv
import re
from functools import partial

def sanitize(str):
    def replaceStartingAndTrailing(search, replace, str):
        last = ''
        new = str
        while(new != last):
            last = new
            new = re.sub('^' + search, replace, last)
            new = re.sub(search + '$', replace, new)
        return new

    sanitizers = [
        lambda x: x.strip(),
        lambda x: x.replace('</div>', '<br/>'),
        lambda x: re.sub(r'<div(.*?)>', '<br/>', x),
        lambda x: x.replace('<br>', '<br/>'),
        lambda x: x.replace('&nbsp;', ' '),
        lambda x: x.replace('"', '\''),
        partial(replaceStartingAndTrailing, r'<br/?>', ''),
        lambda x: x.strip()
    ]
    return reduce(lambda acc, item: item(acc), sanitizers, str)

def getNotesFromCSV(filename):
    elements = {}
    errors = []
    count = -1;
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            count = count + 1
            if count == 0:
                continue
            topic = row[3]
            if topic == '':
                errors.append({'lineNr': count, 'row': row})
                continue
            if topic not in elements:
                elements[topic] = []
            elements[topic].append({
                'title': sanitize(row[0]),
                'content': sanitize(row[1])
            })
    return elements