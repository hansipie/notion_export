import csv
import os
import export

def ExtractData(file):
    dico = {}
    dico["Time"] = os.path.basename(os.path.dirname(file))
    with open(file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        first = 1
        for row in spamreader:
            if first == 1:
                first = 0
                continue
            dico[row[1]] = row[10]
    return dico

def CheckCompatibility(sourceheader, targetfile):
    with open(targetfile, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        

csvdir = export.NotionExport().GetCSVfile()
files=os.listdir(csvdir)
for f in files:
    dico = ExtractData(os.path.join(csvdir, f))

    header = 1
    if os.path.exists('output.csv'):
        header = 0

    with open('output.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=dico.keys())
        if header == 1:
            writer.writeheader()
        writer.writerow(dico)
