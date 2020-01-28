# Verifies the Backfont for size and position
#  

import fontforge
import sys
import csv

#script = sys.argv[0]
#logname = script.split('.')[0]
#sys.stdout = open(logname+".log", "w",encoding="utf-8")

def getUnicode(str):
    #print('getunicode', str)
    a = chr(int(str,16)).encode('utf-8')
    print('getunicode hex:',str,' unicode:', a.hex(), a.decode('utf-8'))
    return a.decode('utf-8')

def listGlyph(font, outfile):
    fw = open(outfile, 'w' ,encoding='utf8', newline='')
    csvWriter = csv.writer(fw)
    #count = 0
    for glyph in font:
        if font[glyph].unicode != -1:
            unicode = hex(font[glyph].unicode)[2:]
            if len(unicode) < 4:
                continue;
            uic = getUnicode(unicode)
            name = font[glyph].glyphname.split('.')[0]
            left, bot, right, top = font[glyph].boundingBox()
            #print(font[glyph].unicode,  font[glyph].glyphname)
            h = round(top-bot,2)
            t = round(top,2)
            b = round(bot,2)
            csvWriter.writerow([uic,unicode,name, h, b,t])
            #count = count + 1
            #if count >9:
            #    break
    
    fw.close()   
    print("Done!  The csv file is in", outfile)
            
for arg in sys.argv:
    print( len(sys.argv),arg)

if len(sys.argv) > 2: 
    fontName  = sys.argv[1]
    outfile = sys.argv[2]
    try:
        font = fontforge.open (fontName)
    except EnvironmentError:
        print('ERROR', EnvironmentError)
        sys.exit (1)

    listGlyph(font, outfile)
else:
    print("\n  SYNTAX: fontforge -script bfwords.py fontforgefile.sfd csvfile.csv")
    print("  Takes data from fontforge file to generate a csv file of unicodes and names")
    print("  i.e.  eb08,Athens")
  
    sys.exit()
