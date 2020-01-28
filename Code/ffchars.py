# routine to change glyph names in font
#  
'''
takes data from fontforge file to generate a list of unicodes and names
i.e.  Athens,eb08

invoke with:
fontforge -script glyphunicode.py  "Sunxxfont.sfd"	"csvfile name"

'''

import fontforge
import sys
import csv

script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open(logname+".log", "w",encoding="utf-8")

charArray = {} 
def getUnicode(str):
    print('getunicode', str)
    a = chr(int(str,16)).encode('utf-8')
    print('getunicode hex:',str,' unicode:', a.hex(), a.decode('utf-8'))
    return a.decode('utf-8')

def write_list(chArray, csvFile, outfile):
    with open(csvFile, 'r' , encoding='utf8') as rr:
        csv_reader = csv.reader(rr)
        with open(outfile, 'w', encoding='utf8', newline='') as ww: # Open a new file named 'new_titanic.csv' under write mode
            csv_writer = csv.writer(ww, delimiter=',') #making use of write method
            for line in csv_reader: # for each file in csv_reader
                print(line[2], line[1])
                l = []
                minb, maxt = getWord(chArray,line[2].strip())
                l.append(line[0])
                l.append(line[1])
                l.append(line[2])
                l.append(minb)
                l.append(maxt)
                #print(l)
                csv_writer.writerow(l) #writing out to a new file from each line of the original file
    rr.close()
    ww.close()
    


def getWord(charTable, word):
    maxt = 0
    minb = 0
    #print('getword',word)
    #try:
    for w in word:
        #print(w, ord(w))
        ww = charArray[w]
        b = ww[0]
        t = ww[1]
        if b < minb:
            minb = b
        if t > maxt:
            maxt = t
        
        #print(ww)
    print('getWord %20s \t%s \t%s'%(word, minb, maxt))
    return minb, maxt
    #except Exception as ex:
    #    print("Parse error on word ",word,w,ex.args)
    #    sys.exit(1)

def buildArray(font):  
    for glyph in font:
        #left, bot, right, top = glyph.boundingBox()
        unicode = font[glyph].unicode
        if unicode > 64 and unicode < 123:
            left, bot, right, top = font[glyph].boundingBox()
            name = font[glyph].glyphname
            print("%s \t %3d : \t % 5d:% 5d:%5d"%(name, font[glyph].unicode, bot,top, top-bot))
            if name == 'underscore':
                name = '_'
            charArray[name] = [bot, top]

        if unicode > 122:
            break

ix = 0
for arg in sys.argv:
    print(ix,arg)
    ix=ix+1
 
if len(sys.argv) >2: 
    csvFile = sys.argv[1]
    ttfFile = sys.argv[2]
    font = fontforge.open(ttfFile) 
    buildArray(font)
    write_list(charArray, csvFile, "sizes.csv")    
    sys.exit(0)
else:
    print("\nsyntax: fontforge -script ffchars.py inputCSVFile ttfFile")
    print("\nCreates a table of metrics of all words usint ttfFile for use by the svg2font.py file")
    sys.exit(1)
