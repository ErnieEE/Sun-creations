#!/usr/bin/env fontforge -lang=py
# http://www.typophile.com/node/81351
# http://fontforge.github.io/scripting.html#Example
# https://fontforge.github.io/python.html
# https://stackoverflow.com/questions/14813583/set-baseline-with-fontforge-scriping
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/

import fontforge
import sys
import os
import csv
import subprocess
import glob

import config as cfg
import util
import logging


script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open('Log\\'+logname+".log", "w",encoding="utf-8")
import logging


script = sys.argv[0]
logname = script.split('.')[0]
file_handler = logging.FileHandler(filename=logname+'.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('LOGGER_NAME')

#logging.basicConfig(level=logging.INFO, file='sample.log')


def svgCopy(svgFile):
    cmd = "copy "+'"'+svgFile+'"'+" svg"
    print(cmd)
    status = subprocess.call(cmd, shell=True)
    if status != 0:    
        print('Error copying ',svgFile)
        sys.exit()

#imagemagic command  = 'convert -font Arial -pointsize 72 caption:%inp4% oxl.pnm'
def makeSVG(fontName, uniName, langName, section):
    print('  makesvg', fontName, ',',uniName, ',',langName,',', section)
    '''if uniName == 'e37e':
        #svgFile = "e37E.svg"
        #svgCopy(svgFile)
        return
    elif uniName == 'e390':
        #svgFile = "e390.svg"
        #svgCopy(svgFile)
        return
    elif uniName == 'ed11':
        #svgFile = "ed11.svg"
        #svgCopy(svgFile)
        return
    else:
    '''
    svgFile = "svg\\"+section+"_"+uniName+".svg"
    
    pattern = "svg\\*_"+uniName+"+*.svg"
    print(pattern);
    if glob.glob(pattern):
        print('file pattern',uniName, 'already exists')
        return
    exists = os.path.isfile(svgFile)
    #print('exists',exists)
    if not exists:
        #ln = langName.replace(" ","_")
        ln = '"'+langName+'"'
        #cmd = "magick convert" + " -font "+fontName+" -pointsize 72 caption:"+langName+" tmp.pnm"
        cmd = "magick convert" + " -font "+fontName+" -pointsize 72 label:"+'"'+langName+'"'+" tmp.pnm"
        print('   ',cmd)
        try:
            status = subprocess.call(cmd, shell=True)
            print('    ',status, cmd)
            if status == 0:
                cmd = "potrace" +" --height 1.0 -s tmp.pnm -o "+'"'+svgFile+'"'
                status = subprocess.call(cmd, shell=True)
                print('    ',status, cmd)
            if status != 0:    
                print('Error processing ', cmd)
                sys.exit(status)
        except:
            print("Error",cmd)
            sys.exit(1)
    else:
        print('    ***duplicate file',svgFile)
        print('    ***Must delete existing files first')
        #sys.exit()

def read_list(fontname, csvFile, cg, namelist=""):
    ixu = int(cg["index_unicode"])   #  index of unicode
    ixn = int(cg["index_name"])      # index of language name
    #ixu = 2     # unicode index
    #ixn = 3         # Language word index
    ixEN = 1    # index of english word

    print('readlist', ixu, csvFile, namelist, ixn)
    with open(csvFile, encoding='utf8') as csvDataFile:
        csvReader = csv.reader(csvDataFile, delimiter=',', quotechar ='"')
        for row in csvReader:
            ncol = len(row)
            row[ixn] = row[ixn].strip()
            row[ixu] = row[ixu].strip()
            name = row[ixn].strip()

            if namelist:
                if row[ixu].lower() not in namelist:
                    #print(ixu,namelist, row[ixu],'not in namelist')
                    continue
            print(row[ixu], row[ixEN], row[ixn], ncol)
            if (len(row) < 3) or (len(row[ixu])) != 4: 
                logging.info('wrong length '+len(row)+' '+len(row[ixu]))
                continue

            if len(name) == 0:
                name = row[ixEN].strip()        
            #print(row[ixn], row[ixu], ncol)   
            print(row[ixn], row[ixu], ncol)
            if len(row[ixu]) < 4:
                makeSVG(fontname, name, name, cg['alias'])
            else:
                makeSVG(fontname, row[ixu], name, cg['alias'])
                
def getConfig(section, language):
    dict = cfg.readConfig()
    sct = section.upper()
    lang = language.lower()
    v = dict[sct][lang]
    print('getconfig',v) 
    return v
    
ix = 0
for arg in sys.argv:
    print(ix,arg)
    ix=ix+1
 
if len(sys.argv) > 3: 
    csvFile = sys.argv[1]
    language = sys.argv[2].lower()
    fontname = sys.argv[3].lower()
    cg = getConfig('langinfo', language)

    if len(sys.argv) > 4:
        index = 0
        namelist = ""
        for arg in sys.argv:
            #print(index, arg)
            if index > 3:
                namelist = namelist+'+'+arg.strip()
            index += 1
        print('namelist =',namelist)     
        read_list(fontname, csvFile, cg, namelist.lower())
    else:
        print('whole thing')
        read_list(fontname, csvFile, cg, "")

else:
    print("\nsyntax: fontforge -script csv2svg.py csvfile  Language fontfile [unicode list]")
    print("   - script Python script file,  csvfile language fontfile")
    print("   optional space separated unicode list i.e. e000 eda5")
    print("\nCreates svg files in the /svg directory using")
    print("the names in the csv file")
    print("The csv file format ")
    print("      glyph, unicode(hex), name")
    print("Optionally limits build to list of unicodes")
    logging.error("SYNTAX Error")
    sys.exit(1)

print('done')
