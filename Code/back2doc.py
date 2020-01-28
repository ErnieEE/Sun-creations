# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import fontforge
import sys
import csv
#import codecs

script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open(logname+".log", "w",encoding="utf-8")

def getUnicode(str):
    print('getunicode', str)
    a = chr(int(str,16)).encode('utf-8')
    print('getunicode hex:',str,' unicode:', a.hex(), a.decode('utf-8'))
    return a.decode('utf-8')
    
def int2Unicode(str):
    print('int2unicode', str)
    a = str.encode('utf-8')
    print('getunicode hex:',str,' unicode:', a.hex(), a.decode('utf-8'))
    return a.decode('utf-8')

index_other = 0
index_name = 2
index_unicode = 1

def xread_list(namelist, outfile):
    fr = open(namelist, 'r')
    fw = open(outfile, 'w' ,encoding='utf8')
    csvReader = csv.reader(fr, delimiter=',')
    csvWriter = csv.writer(fw, delimiter=',', lineterminator='\n')
    for row in csvReader:
        l = len(row)
        print(l, row[l-1],'|')
            
        if row[0] != '#':
            #print(row)
            uic = row[1].strip()
            unicode = getUnicode(uic)
            #print(unicode)
            row[0] = unicode
            row.append(unicode)
            csvWriter.writerow(row)
 
    fr.close
    fw.close()
    
# parse kmn file and generate csv file for documentation
def read_csv(namelist, outfile):
    print('read_csv',namelist,outfile)
    #fr = open(namelist, 'r', encoding='utf8')
    #fw = open(outfile, 'w' , encoding='utf8')
    fr = open(namelist, 'r', encoding='utf8')
    fw = open(outfile, 'w' , encoding='utf8')
    csvReader = csv.reader(fr, delimiter=',')
    for row in csvReader:
        print(row);
        uic = row[1].strip()
        if uic != "":
            unicode = getUnicode(uic)
            fw.write(unicode)
    fr.close
    fw.close()
'''  
def getUnicode(str):
    print('getunicode', str)
    a = chr(int(str,16)).encode('utf-8')
    print('getunicode hex:',str,' unicode:', a.hex(), a.decode('utf-8'))
    return a.decode('utf-8')
'''
  
def getGlyphs(font, outfile):
    fw = open(outfile, 'w' ,encoding='utf8')
    for glyph in font:
        if font[glyph].unicode != -1:
            print(font[glyph].unicode, font[glyph].glyphname)
            uic = font[glyph].unicode
            unicode = int2Unicode(uic)
            #print(uic, unicode, font[glyph].glyphname)
            #fw.write(uic+' ')
    fw.close()
    
    
if len(sys.argv) > 1: 
    infile = sys.argv[1]
    outfile = sys.argv[2]
else:
    infile = str(input("enter font(sfd) file"))
    outfile = str(input("enter text output file name"))

print (sys.version)
read_csv(infile, outfile)

