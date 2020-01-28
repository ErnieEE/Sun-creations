#!/usr/bin/env fontforge -lang=py
# http://www.typophile.com/node/81351
# http://fontforge.github.io/scripting.html#Example
# https://fontforge.github.io/python.html
# https://stackoverflow.com/questions/14813583/set-baseline-with-fontforge-scriping
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/
# http://designwithfontforge.com/en-US/Importing_Glyphs_from_Other_Programs.html
#https://pelson.github.io/2017/xkcd_font_raster_to_vector_and_basic_font_creation/

import fontforge
import sys
import csv

import os.path
from os import walk
import config as cfg

script = sys.argv[0]
logname = script.split('.')[0]
#sys.stdout = open(logname+".log", "w",encoding="utf-8")

ffMetrics = {}  # font metrics taken from font
llMetrics = {}  # config file language metrics

def getWord( word):
    return wordTable[word]
    print(word, minb, maxt)
    return minb, maxt

def char_table(str):
    asc = 0
    dsc = 0
    for ch in str:
        if (ch.isupper()):
            asc = 1
        if (ch in llMetrics["char_ascent"]):
            asc = 1
        if (ch in llMetrics["char_descent"]):
            dsc = 1
    #print('char_table word=%s asc=%s dsc=%s'%(str, asc, dsc))
    return asc, dsc
'''    
   Font         ascent  _____
   Metrics      xheight _____   scale = 200/xheight
   scaling      base    _____   height =200  scale = xheight / 200
                descent _____   d = font_descender / scale
                
   wordMax and wordMin are whole word metrics calculated from font for each word
   ff_asc, ff_dsc, ff_height taken from the defult font metrics for all of font
'''
font_ascender = 75
font_descender = 75
max_ascent = 1420

def getWord(word):
    maxt = 0
    minb = 0
    print('getword',word)
    #try:
    ww = []
    for w in word:
        print(w)
        g = ttfFont[ord(w)]
        name = g.glyphname
        print('g', w, ord(w),g.glyphname, g.unicode)
        left, bot, right, top = g.boundingBox()
        name = g.glyphname
        print("%s \t %3d : \t % 5d:% 5d:%5d"%(name, g.unicode, bot,top, top-bot))
        ww = [bot, top]
        b = ww[0]
        t = ww[1]
        if b < minb:
            minb = b
        if t > maxt:
            maxt = t
        
        #print(ww)
    print('getWord %20s \t%s \t%s'%(word, minb, maxt))
    return minb, maxt



def scale(glyph):   #, wordMin, wordMax):
    global desc_scale
    wordMin, wordMax = getWord(glyph.glyphname)
    print('word size', wordMin, wordMax, wordMax-wordMin)
    #ffAsc = ffMetrics['ascender'] - ffMetrics['xheight']
    #wAsc = wordMax - ffMetrics['xheight']
    #dscR = wordMin / ffMetrics['descender']
    #ascR = wAsc / ffAsc
    #ffH = ffAsc - ffMetrics['descender']
    print('FFMetrics', ffMetrics['descender'],ffMetrics['ascender'],ffMetrics['xheight'])
    print('wordMetrics', wordMin, wordMax)
    printBound(glyph,'Image Size')
    iL, iB, iR, iT = glyph.boundingBox()

    # scale to word
    iH = iT - iB
    wH = wordMax - wordMin
    wScale = wH/iH
    print('word Scale ih %s wh %s wscale %s'%(round(iH,2), round(wH, 2), round(wScale,2)))
    scale_matrix = psMat.scale(wScale)
    glyph.transform(scale_matrix)
    printBound(glyph,'Scaled to Word')
    #sL, sB, sR, sT = glyph.boundingBox()
    
    s = 200/ffMetrics['xheight']
    print('scale to FF',round(s,2))
    scale_matrix = psMat.scale(s)
    glyph.transform(scale_matrix)
    
    # move image vertically 
    printBound(glyph,'Scaled to FF')
    sL, sB, sR, sT = glyph.boundingBox()
    y = 300 - sB + (wordMin * s)
    base_matrix = psMat.translate(0, y)
    glyph.transform(base_matrix)
    print('move y: %s bot: %s desc:%s'%(round(y,2), round(sB,2), round((wordMin*s),2)))
    printBound(glyph,'Moved ')
 
def printBound(glyph, comment = ""):
    left, bot, right, top = glyph.boundingBox()
    #print("boundbox height width",round(top-bot,2), round(right-left,2))
    print(comment,'bound height:', round((top-bot),2), 'bot:',round(bot,2), 'top:',round(top,2), 'width:',round((right-left),2),'lb:',round(glyph.left_side_bearing,2), 'rb:',round(glyph.right_side_bearing,2))
    
def setBearing(glyph):
    left, bot, right, top = glyph.boundingBox()
    width = right - left
    #print('bearing lb rb left right', round(glyph.left_side_bearing,2), round(glyph.right_side_bearing,2), round(left, 2), round(right,2), round(width,2))
    '''  s = 1.0
    if width > 1200:
        s = 1200/width
    elif width > 1100:
        s = 1100/width
    elif width > 1000:
        s = 1000/width
    elif width > 800:
        s = 800/width
     
    scale_matrix = psMat.scale(s, 1.0)
    glyph.transform(scale_matrix)
    '''
    #print('new width', round(glyph.width,2), round(s, 2));
    left, bot, right, top = glyph.boundingBox()
    glyph.width = right - left+ 150
    glyph.left_side_bearing = 75
    glyph.right_side_bearing = 75
    print('bearing', round(glyph.left_side_bearing,2), round(glyph.right_side_bearing,2), round(right-left, 2))
     
def xmove(glyph):
    left, bot, right, top = glyph.boundingBox()
    y = 300 - bot - desc_scale

    base_matrix = psMat.translate(0, y)
    glyph.transform(base_matrix)
    #left, bot, right, top = glyph.boundingBox()
    #print('move:bot', round(bot,2), 'height = ', round((top-bot),2))

def addFont(font, unicode, section, imagename):  #, mn, mx) :
    print("------------------------------------")
    if unicode == 'e37e':
        file = "svg\\e37E+period.svg"
        glyph = font.createChar(int(unicode, 16))
        glyph.importOutlines(file)  
        return
    elif unicode == 'e390':
        file = "svg\\e390+possessive.svg"
        glyph = font.createChar(int(unicode, 16))
        glyph.importOutlines(file) 
        return
    elif unicode == 'ed11':
        file = "svg\\ed11+pn.svg"
        glyph = font.createChar(int(unicode, 16))
        glyph.importOutlines(file) 
        return
    else:
        file = "svg\\"+section+"_"+unicode+"+"+imagename+".svg"
        print('addFont file', file, unicode)
        if unicode == -1:
            glyph = font.createChar(-1, imagename)
        else:
            glyph = font.createChar(int(unicode, 16))
        glyph.importOutlines(file)  
        glyph.glyphname = imagename
        scale(glyph)    #, mn, mx)
        #ove(glyph)
        setBearing(glyph)
        #printBound(glyph, imagename)    
   
def createFont(backfont):    #, ver, section):
    #fontname = 'SUNBF'+ver+'_'+section
    f = backfont.split('.')
    fontname = f[0]
    ascent = 1000
    descent = 800
    em = 1000
    encoding = "Custom"
    weight = "Regular"
    font = fontforge.font()
    font.fontname = fontname
    font.familyname = fontname
    font.fullname = fontname
    font.ascent = ascent
    font.descent = descent
    font.em = em
    font.encoding = encoding
    font.weight = weight
    font.save(backfont)

    return font

def openFont():
  font = fontforge.open(fontname)
  return font

def genFont(fnt):
    #fontname = 'SUNBF'+ver+'_'+fnt
    font.generate(fnt)   

def read_list(font, csvFile, namelist=""):
    print('readlist',csvFile, namelist)
    ixu = int(llMetrics["index_unicode"])
    ixn = int(llMetrics["index_name"])
    with open(csvFile, encoding='utf8') as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',', quotechar ='"') 
        for row in csvReader:
            #print(len(row), row)
            if (len(row) < 3) or (len(row[ixu])) != 4: 
                continue
            ncol = len(row)
            unicode = row[ixu].lower()
            name = row[ixn]
            if namelist:
                if unicode not in namelist:
                    continue
            #print(row[ixn], row[ixu], ncol) 
            unicode = row[ixu].lower()
            name = row[ixn]   
            #mn = row[3].strip()         # the descent of word
            #mx = row[4].strip()         # the ascent of word
            addFont(font, unicode, section, name)   #, float(mn), float(mx))


    
def getMetrics(ttfFont, language):
    global ffMetrics
    global llMetrics
    #font = fontforge.open(fontfile)
    #print('ffmetrics ascent= %s descent= %s xHeight= %s'%(font.os2_typoascent, font.os2_typodescent, font.xHeight))
    v = {}
    v['file'] = ttfFile
    v['xheight'] = float(ttfFont.xHeight)
    v['ascender'] = float(ttfFont.os2_typoascent)
    v['descender'] = float(ttfFont.os2_typodescent)
    ffMetrics = v
    print('ffmetrics ascent= %s descent= %s xHeight= %s'%(v['ascender'], v['descender'], v['xheight']))
 
    dict = cfg.readConfig()
    llMetrics = dict["LANGINFO"][language.lower()]
    
x = 0      
for arg in sys.argv:
    print( x,arg)
    x=x+1
print(len(sys.argv))
if len(sys.argv) > 4: 
    ver = sys.argv[1]
    csvFile = sys.argv[2]
    ttfFile = sys.argv[3]
    ttfFont = fontforge.open(ttfFile) 
    language = sys.argv[4].upper()
    getMetrics(ttfFont, language)
    section = llMetrics['alias']
    #fnt = ttfFile.split('.')
    backFont = "SUNBF"+ver+"_"+section+".sfd"
    fnt = backFont.split('.')
    font = createFont(backFont)     #, ver, section)
    
    if len(sys.argv) > 5:
        index = 0
        namelist = ""
        for arg in sys.argv:
            print(index, arg)
            if index > 4:
                nl = arg.strip().lower()
                namelist = namelist+'+'+nl
            index += 1
        print('namelist =',namelist)     
        #processUnnamedGlyphs(font, m, sct, namelist)
        read_list(font, csvFile, namelist)
    else:
        print('whole thing')
        read_list(font, csvFile, "")
    
    genFont(fnt[0]+".ttf")
else:
    print("\nsyntax: fontforge -script svg2Font.py backFont.sfd csvfile fontfile  Language [unicode list]")
    print("   Creates a back font from the svg files in /svg directory")
    print("   using the names in the kmn file for font characteristics")
    print("   Optionally limits build to list of unicodes")
    print("   -script Python script file,  Fontforge file  csvfile( The dictionary file)")
    print("   language 2 character i.e. EN")
    print("   optional space separated unicode list i.e. e000 eda5")
    print("   The csv file is expected to have english name in")
    print("      glyph in column 0, english word in column 1, unicode in column 2 and")
    print("    language words in column 3. \n   Optionally limits build to list of unicodes")
    sys.exit()

font.save(backFont)
print('saved font',backFont)

    