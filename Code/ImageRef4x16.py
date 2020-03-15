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
sys.stdout = open('Log\\'+logname+".log", "w",encoding="utf-8")

IMAGEPOS = 0
LANGNAMEPOS = 2
UECPOS = 1
ENNAMEPOS = 2

COLUMNS = 4
ROWSPERPAGE = 16


def convert2csv(filename):
	print('convert2csv ', filename)
	#result = subprocess.call(["C:\Program Files\LibreOffice\program\soffice", "--headless", "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true", filename])
	command = '"C:\Program Files\LibreOffice\program\soffice",  "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true", '+ filename
	print(command)
	result = subprocess.call(["C:\Program Files\LibreOffice\program\soffice",  "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true", filename])

	print('convert2csv ', result)

def convert2ods(filename):	
	print('convert2ods ', filename)
	result = subprocess.call(["C:\Program Files\LibreOffice\program\soffice", "--headless", "--convert-to", "ods", "--infilter=CSV:44,34,76,1,,,true", filename])
	print('convert2ods ', result)
	
#symbol unicode name
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
       
def createCell(row):
    name = row[LANGNAMEPOS]
    uec = row[UECPOS]
    image = row[IMAGEPOS]
    #syn = row[SYNPOS]
    line = image+',"'+name+'\n('+uec+')"'    #,'+syn;
    return line

def writexref(ddata, csv_out):
    #d = sorted(ddata, key=lambda x: x[NAMEPOS].lower())
    print(ddata)
    d = ddata
    dlen = len(d)
    with open(csv_out, 'w' , encoding="utf-8") as outfile:
        count = 0
        for y in range(0, len(d),64):
            for x in range(y, y+16):
                #print('y',y,'x',x)
                #print('y',y','x',x,len(d), x+16, x+32, x+48)
                print(dlen,'y',y,':','x',x,x+16, x+32, x+48)
                line = ""
                if x < dlen - 1:
                    line = createCell(d[x])
                if x+16 < dlen - 1:  
                    line = line + ','+createCell(d[x+16])
                if x+32 < dlen - 1:  
                    line = line + ','+createCell(d[x+32])    
                if x+48 < dlen - 1:  
                    line = line + ','+createCell(d[x+48])    
                '''
                if x+48 > dlen-1:
                    print('>48')
                    line = createCell(d[x])+','+createCell(d[x+16])+','+createCell(d[x+32])
                else:    
                    line = createCell(d[x])+','+createCell(d[x+16])+','+createCell(d[x+32])+','+createCell(d[x+48])
                '''
                outfile.write(line+',')
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
'''
x0 = [csv_data[index] for index in range(0, len(csv_data), 16)]
x1 = [csv_data[index] for index in range(1, len(csv_data), 16)]
x2 = [csv_data[index] for index in range(2, len(csv_data), 16)]
x3 = [csv_data[index] for index in range(3, len(csv_data), 16)]
print(x0)
print('--------')
print(x1)
'''
name_sort = sorted(csv_data, key=lambda x: x[LANGNAMEPOS].lower())
writexref(name_sort, csv_out)
convert2ods(csv_out)


print("-------- Done ----------")
print("Create a libreoffice richtext document")
print("Load, csv_out.ods into a libreoffice calc spreadsheet")
print("Load SUN font.  Resize image columns font size to 32. ")
print("Print output should be 4 columns with 16 rows per page.")
print("Cell format image column width = .65 text column width = 1.15")
print("margins left and right = .5. Set name columns to wrap")
print("Export as pdf")