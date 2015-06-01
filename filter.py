__author__ = 'ignacioelola'

import csv
import sys

with open("data/output.csv", "r") as infile:
    with open("data/filtered-output.csv", "w") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            if str(sys.argv[1]) in row[2].lower():
                writer.writerow(row)
