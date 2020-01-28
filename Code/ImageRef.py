"""
 Creates a condensed view of the dictionary  with the unicode and name in same column

   fontforge -script imageref.py infile outfile')
     Example: fontforge -script genesis.csv genout.csv\n')

"""

import sys
import io		#python 2
import subprocess
import csv
#import tkinter
#import tkinter.filedialog

script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open(logname+".log", "w",encoding="utf-8")

IMAGEPOS = 0
NAMEPOS = 2
UECPOS = 1
SYNPOS = 3

def convert2csv(filename):
	result = subprocess.call(["C:\Program Files\LibreOffice\program\soffice", "--headless", "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true", filename])
	print(result)
	
def read_csv_data(path):
    f = open(path, 'r', encoding="utf-8")
    #data = csv.reader(f, delimiter=',', quotechar='"')
    csvReader = csv.reader(f, delimiter=',', quotechar='"')
    print('csvread',path)
    # Assume no column names
    data_lines = []
    for row in csvReader:
        data_lines.append(row)
    return data_lines			

def xget_nth(haystack, needle, n):
	if n == 1:
		return haystack.find(needle)
	else:
		return haystack.find(needle, get_nth(haystack, needle, n - 1) + 1)

def writexref(ddata, csv_out):
    name_sort = sorted(ddata, key=lambda x: x[NAMEPOS].lower())
    with open(csv_out, 'w' , encoding="utf-8") as outfile:
        count = 0
        for row in name_sort:
            name = row[NAMEPOS]
            uec = row[UECPOS]
            image = row[IMAGEPOS]
            #syn = row[SYNPOS]
            line = image+',"'+name+'\n('+uec+')"'    #,'+syn;
            outfile.write(line+',')
            count = count + 1
            #print(count, count %4)
            if count % 4 == 0:
                outfile.write('\n')
			
csv_file = ""
csv_out = ""
for arg in sys.argv:
    print( arg)

if len(sys.argv) > 1: 
    csv_file = sys.argv[1]
    csv_out = sys.argv[2]
else:
    print('\nCreates a condensed view of the dictionary  with the unicode and name in same column');
    print('>>  fontforge -script imageref.py infile outfile')
    print('>>  Example: fontforge -script genesis.csv genout.csv\n')
    exit()
  

csv_data = read_csv_data(csv_file)
writexref(csv_data, csv_out)
print("-------- Done ----------")
print("Create a libreoffice richtext document")
print("Load", csv_out,"into a libreoffice calc spreadsheet")
print("resize image columns to 32.  resize other columns")