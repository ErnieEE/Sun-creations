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
import time
import glob
import traceback
from util import log_info, log_err, log_warn, new_logger, closeLoggers
from bfConfig import readCfg  

#imagemagic command  = 'convert -font Arial -pointsize 72 caption:%inp4% oxl.pnm'
def makeSVG(fontName, uniName, name, alias):
    #log_info('  makesvg', fontName, ',',uniName, ',',name,',', alias)
    if uniName == 'e37e':
        svgFile = "e37e_period.svg"
        log_info("using existing file",svgFile)
        #svgCopy(svgFile)
        return
    elif uniName == 'e390':
        svgFile = "e390_possesive.svg"
        log_info("using existing file",svgFile)
        #svgCopy(svgFile)
        return
    elif uniName == 'ed11':
        svgFile = "ed11_pn.svg"
        log_info("using existing file",svgFile)
        #svgCopy(svgFile)
        return
    else:
        svgFile = "svg\\"+alias+"_"+uniName+".svg"
        #pnmFile  = "svg\\"+alias+"_"+uniName+".pnm"
        pnmFile = "tmp.pnm"
        pattern = "svg\\*_"+uniName+"+*.svg"
        #log_info(pattern);
        if glob.glob(pattern):
            log_warn('file pattern',uniName, 'already exists')
            return
        exists = os.path.isfile(svgFile)
        #log_info('exists',exists)
        if not exists:
            #cmd = "magick convert" + " -font "+fontName+" -pointsize 72 label:"+'"'+name+'"'+" tmp.pnm"
            cmd = "magick convert" + " -font "+fontName+" -pointsize 72 label:"+'"'+name+'"'+" "+pnmFile
            log_info('   ',cmd)
            try:
                status = subprocess.call(cmd, shell=True)                #cmd = "potrace" +" --height 1.0 -s tmp.pnm -o "+'"'+svgFile+'"'
                cmd = "potrace" +" --height 1.0 -s "+pnmFile+" -o "+'"'+svgFile+'"'
                log_info('    ',status, cmd)
                if status == 0:
                    status = subprocess.call(cmd, shell=True)
                    #log_info('    ',status, cmd)
                if status != 0:    
                    log_err('Error processing ',status, cmd)
                    return(status)
            except Exception as  e:
                log_err("fatal error makeSVG file =", svgFile,e)
                traceback.print_exc()
                return(2)
        else:
            log_warn('    ***duplicate file',svgFile)  #, file=sys.stderr)
            #time.sleep(0.1)
            #log_warn('    ***Must delete existing files first')  #file=sys.stderr)
            #sys.stdout.flush()
            #return()

def read_list(fontname, csvFile, namelist=""):
    #cfg = json.load(open('config.json'))
    cfg = readCfg()
    alias = cfg["alias"]
    ixu = cfg["langColumns"]["index_unicode"]
    ixn = cfg["langColumns"]["index_langName"]

    try:
        log_info('readlist',fontname, csvFile, namelist)
        with open(csvFile, encoding='utf8') as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=',', quotechar ='"')
            for row in csvReader:
                #log_info('|'+alias+'|',row, ixn, ixu)
                ncol = len(row)
                name = row[ixn].strip()
                unicode = row[ixu].strip().lower()

                if namelist:
                    if unicode not in namelist:
                        #log_info(ixu,namelist, row[ixu],'not in namelist')
                        continue
                #log_info(name, unicode, ncol)
                if (len(row) < 3) or (len(row[ixu])) != 4: 
                    logging.info('wrong length '+len(row)+' '+len(row[ixu]))
                    continue

                #if len(name) == 0:
                #    name = row[ixEN].strip()        
                 
                #log_info(name, unicode, ncol)
                if len(unicode) < 4:
                    makeSVG(fontname, name, name, alias)
                else:
                    makeSVG(fontname, unicode, name, alias)
                time.sleep(0)   # allow interrupts
                
    except Exception as e:
        log_err("fatal error read_list",e)   # file=sys.stderr)
        traceback.print_exc()
        return(3)
                
def xgetConfig(section, language):
    dict = cfg.readConfig()
    sct = section.upper()
    lang = language.lower()
    v = dict[sct][lang]
    log_info('getconfig',v) 
    return v

def main(*ffargs):   
    new_logger("csv2svg")   
    ix = 0
    args = []
    for a in ffargs[0]:
        log_info(ix,a)
        args.append(a)
        ix=ix+1

    if len(args) > 2: 
        csvFile = args[1]
        #alias = sys.argv[2].upper().strip()
        ttfFont = args[2].lower()
        #cg = getConfig('langinfo', language)
        namelist = ""
        if len(args) > 3:
            index = 0
            for arg in args:
                #log_info(index, arg)
                if index > 2:
                    namelist = namelist+'+'+arg.strip()
                index += 1
                
            if len(namelist) < 4:
                namelist = ""

        read_list(ttfFont, csvFile, namelist.lower())

    else:
        log_info("\nSYNTAX Error")
        log_info("\nsyntax: fontforge -script bfv2svg.py csvfile ttffile [unicode list]\n")
        log_info("   - script Python script file,  csvfile language fontfile\n")
        log_info("   optional space separated unicode list i.e. e000 eda5\n")
        log_info("\nCreates svg files in the /svg directory using\n")
        log_info("the names in the csv file\n")
        log_info("The csv file format \n")
        log_info("      glyph, unicode(hex), name\n")
        log_info("Optionally limits build to list of unicodes\n")
        return(1)

    log_info('Done SVG files are in svg directory')
    closeLoggers(__name__)
    return 0

if __name__ == "__main__":
   
    print('name main',type(sys.argv),sys.argv)
    main(sys.argv)    