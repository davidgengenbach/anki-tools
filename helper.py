import csv
import shutil
import io

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

def backup_folder(folder, backup_folder = None):
	name = folder.rsplit('/', 1)[-1]
	backup_folder = '{}/{}_{}'.format(backup_folder, name, get_timestamp())
	shutil.copytree(folder, backup_folder)

def get_timestamp(format = "%y%m%d__%H:%M:%S"):
	from time import gmtime, strftime
	return strftime(format, gmtime())

def linebreak_to_html(x):
	return x.replace('//', '<br/>')

def linebreak_to_txt(x):
	return x.replace('<br/>', '//')

def write_file(file, data):
    with open(file, 'w') as f:
        f.write(data)