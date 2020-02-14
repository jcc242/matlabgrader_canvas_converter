from os import listdir
from os.path import isfile, join
import csv

def load_file(filename):
    with open(filename, "r") as f:
        return f

def parse_csv(filehandle):
    reader = csv.reader(filehandle)
    next(reader)
    return [row for row in reader]

def get_csv_files(path):
    print("path: {}".format(path))
    outfiles = []
    for myfile in listdir(path):
        if myfile.endswith(".csv"):
            outfiles.append(join(path, myfile))
