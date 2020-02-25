from os import listdir
from os.path import isfile, join
import csv

def load_file(filename):
    with open(filename, "r") as f:
        return f

def parse_csv(filehandle):
    reader = csv.reader(filehandle, delimiter=',')
    next(reader)
    return [row for row in reader]

def csv_headers(filehandle):
    reader = csv.reader(filehandle)
    header = next(reader)
    return header

def column_index(columnHeader, key):
    assert key in columnHeader, "Key not found in csv header"
    return columnHeader.index(key)

def get_csv_files(path):
    print("path: {}".format(path))
    outfiles = []
    for myfile in listdir(path):
        if myfile.endswith(".csv"):
            outfiles.append(join(path, myfile))
