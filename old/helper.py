import csv
import os
import re
from functools import partial

def getFilename(path):
    filename = os.path.basename(path);
    return {
        'filename': file,
        'filenameWithoutExtension': os.path.splitext(filename)[0]
    }

def getNotesFromTxt(filename):
    p = re.compile('"(.*)","(.*)"(\r\n)?$')
    count = 0;
    elements = []
    errors = []
    with open(filename, 'r') as file:
        for line in file:
            count = count + 1
            matched = p.search(line)
            if not matched:
                errors.append({"lineNr": count, "line": line})
                continue
            title = matched.group(1)
            content = matched.group(2)
            elements.append({'title': title, 'content': content})
    return (elements, errors)

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
        lambda x: re.sub(r'<br.?>', '<br/>', x),
        lambda x: x.replace('&nbsp;', ' '),
        lambda x: x.replace('<br />', '<br/>'),
        lambda x: x.replace('"', '\''),
        lambda x: re.sub(r'(?:<br ?/?>){3,}', '<br/><br/>', x),
        partial(replaceStartingAndTrailing, r'<br ?/?>', ''),
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
            # Ignore header
            if count == 0:
                continue
            if len(row) != 4:
                print '(Line: {}) Error in row - len(row) {} not right: {}'.format(count, len(row), row)
                errors.append({
                    'type': 'len(row) wrong',
                    'line': count,
                    'row': row
                })
                continue
            topic = row[3]
            if topic == '':
                print '(Line: {}) Error in row - topic is empty: {}'.format(line, row)
                errors.append({
                    'type': 'topic empty',
                    'line': count,
                    'row': row
                })
                continue
            if topic not in elements:
                elements[topic] = []
            elements[topic].append({
                'title': sanitize(row[0]),
                'content': sanitize(row[1])
            })
    return elements

def getDuplicates(elements):
    keys = map(lambda x: x['title'], elements)
    duplicates = set([x for x in keys if keys.count(x) > 1])
    return duplicates