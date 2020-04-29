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
from tkinter import *
import traceback
import json
from util import log_info, log_err, new_logger, closeLoggers
#from bfConfig import cfg as cg
from array2xlsx import array2xlsx

def getUnicode(str):
    try:
        a = chr(int(str,16)).encode('utf-8')
        return a.decode('utf-8')
    except Exception as  e:
        log_err("fatal error getUnicode",e)
        return 1

def listGlyphs(font):
    cfg = json.load(open('config.json'))
    IMAGEPOS = cfg["enColumns"]["index_font"]
    LANGNAMEPOS = cfg["langColumns"]["index_langName"]
    UECPOS = cfg["langColumns"]["index_unicode"]
    ENNAMEPOS = cfg["langColumns"]["index_name"]
    
    glyphs = []
    for glyph in font:
        gl = [None, None, None]
        try:
            if font[glyph].unicode != -1:
                unicode = hex(font[glyph].unicode)[2:]
                if len(unicode) < 4:
                    continue;
                uic = getUnicode(unicode)
                name = font[glyph].glyphname.split('.')[0]
                log_info(uic.encode().hex(),unicode, name)
                gl[IMAGEPOS] = uic
                gl[ENNAMEPOS] = name
                gl[UECPOS] = unicode
                glyphs.append(gl)
                 
        except Exception as e:
            log_err("fatal error listGlyph",e)
            traceback.print_exc()
            return 1
    
    #sort by name        
    name_sort = sorted(glyphs, key=lambda x: x[ENNAMEPOS].lower())
    return name_sort

def writeGlyphs(glyphs, outfile):
    print('wrg',outfile)
    fw = open(outfile, 'w' ,encoding='utf8', newline='')
    csvWriter = csv.writer(fw)
    count = 0
    for g in glyphs:
        try:
            csvWriter.writerow(g)
        except Exception as e:
            log_err("fatal error writeGlyphs",e)
            traceback.print_exc()
            return 2
    
    fw.close()   
    
def main(*ffargs):
    new_logger("sfd2csv")    
    args = []
    
    for a in ffargs[0]:
        log_info(a)
        args.append(a)

    if len(args) > 2: 
        fontName  = args[1]
        outfile = args[2]
        try:
            font = fontforge.open (fontName)
            glyphs = listGlyphs(font)
            writeGlyphs(glyphs, outfile)
            array2xlsx(glyphs, outfile.split('.')[0]+'.ods')
        except Exception as e:
            log_err("fatal error ",e)
            traceback.print_exc()
            return 1
    else:
        log_info("\n  SYNTAX: fontforge -script sfd2csv.py fontforgefile.sfd csvfile.csv")
        log_info("  Takes data from fontforge file to generate a csv file of symbols,")
        log_info("  unicodes and names")
        log_info("  i.e. symbol,eb08,Athens")
        return 1
        
    log_info("Done!  The csv file is in", outfile)
    closeLoggers(__name__)
    
    return 0
if __name__ == "__main__":
   
    print('name main',type(sys.argv),sys.argv)
    main(sys.argv)    