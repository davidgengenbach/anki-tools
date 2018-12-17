import csv
import shutil
import io
import os
import re

csv_kwargs = dict(delimiter=',', quotechar='"')
csv_writer_kwars = dict(quoting=csv.QUOTE_ALL, **csv_kwargs)


def get_csv(file):
    with open(file) as f:
        reader = csv.reader(f, **csv_kwargs)
        return list(reader)


def to_csv(rows):
    o = io.StringIO()
    w = csv.writer(o, **csv_writer_kwars)
    w.writerows(rows)
    return o.getvalue().strip()


def write_csv(file, rows):
    write_file(file, to_csv(rows))


def backup_folder(folder, backup_folder=None):
    name = folder.rsplit('/', 1)[-1]
    backup_folder = '{}/{}_{}'.format(backup_folder, name, get_timestamp())
    shutil.copytree(folder, backup_folder)


def get_timestamp(format="%y%m%d__%H:%M:%S"):
    from time import gmtime, strftime
    return strftime(format, gmtime())


def linebreak_to_html(x):
    return x.replace('//', '<br/>')


def linebreak_to_txt(x):
    return replace(x, [
            ('<br/>', '//'),
            ('<br>', '//'),
            ('<br />', '//')
        ])

def linebreak_to_real(x):
    return replace(x, [
        ('//', '\n'),
        ('<br/>', '\n'),
        ('<br>', '\n'),
        ('<br />', '\n')
    ])


def write_file(file, data):
    with open(file, 'w') as f:
        f.write(data)

def remove_file(file):
    if os.path.exists(file):
        os.unlink(file)

def get_filename(file, with_extension=True):
    filename = file.rsplit('/', 1)[1]
    if not with_extension:
        filename = filename.rsplit('.', 1)[0]
    return filename


def replace(x, replacements):
    for replacement in replacements:
        if not isinstance(replacement, tuple):
            replacement = (replacement, '')
        a, b = replacement
        x = x.replace(a, b)
    return x


def remove_trailing_linebreaks(x):
    return re.sub(r'(\/{2})+$', '', x)

def remove_preceding_linebreaks(x):
    return re.sub(r'(^\/{2})+', '', x)


def join(x, delimiter='//'):
    return delimiter.join(x).strip()


def get_default_db_path():
    return os.path.join(os.path.expanduser("~"), '.local/share/Anki2/User 1/collection.anki2')


def txt_lines_to_csv(x):
    fns = [
        join,
        remove_preceding_linebreaks,
        remove_trailing_linebreaks,
        lambda x: x.replace('[[', '<b>').replace(']]', '</b>') 
    ]
    for fn in fns: x = fn(x)
    return x


def csv_line_to_txt(x):
    fns = [
        linebreak_to_real,
        lambda x: x.replace('<div>', '\n').replace('</div>', '\n'), 
        lambda x: x.replace('<b>', '[[').replace('</b>', ']]') 
    ]
    for fn in fns: x = [fn(y) for y in x]
    x = '((\n{}\n))\n{}\n'.format(*x)
    return x
