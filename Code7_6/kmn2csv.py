# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import fontforge
import sys
import csv
import traceback
from util import log_info, log_err, getUnicode, new_logger, closeLoggers
from bfConfig import readCfg 
#from bfConfig import bfClass as bf
from array2xlsx import array2xlsx

'''
def getUnicode(str):
    #log_info('getunicode', str)
    a = chr(int(str,16)).encode('utf-8')
    #log_info('getunicode hex:'+str+' unicode:'+ a.hex())  # "+' '+a.decode('utf-8'))
    return a.decode('utf-8')
'''
   
# parse kmn file and generate csv file for documentation
def read_kmn(namelist, outfile):
    #cfg = json.load(open('config.json'))["enColumns"]
    cfg = readCfg()["enColumns"]
    kmnAry = []
    fr = open(namelist, 'r')
    fw = open(outfile, 'w' ,encoding='utf8')
    csvReader = csv.reader(fr, delimiter='+')
    csvWriter = csv.writer(fw, delimiter=',', lineterminator='\n')
    for row in csvReader:
        l = len(row)
        if l == 3:
            if '>'  in row[1]:
                csvRow = [None, None, None]
                #log_info(row)
                unicode = row[2].strip().strip('\"').strip("\'").lower()
                uic = getUnicode(unicode)
                name = row[0].strip().strip('\"').strip("\'")
                csvRow[cfg["index_font"]] = uic
                csvRow[cfg["index_name"]] = name
                csvRow[cfg["index_unicode"]] = unicode
                log_info(uic.encode().hex(),unicode, name)
                kmnAry.append(csvRow)
                csvWriter.writerow(csvRow)

    fr.close()
    fw.close()
    return kmnAry

def main(*ffargs):
    new_logger("kmn2csv")    

    ix = 0
    args = []
    for a in ffargs[0]:
        log_info(ix,a)
        args.append(a)
        ix=ix+1

    if len(args) == 3: 
        namelist = args[1]
        outFile = args[2]
        try:
            kmnAry = read_kmn(namelist, outFile)
            array2xlsx(kmnAry, outFile.split('.')[0]+'.ods')
        except Exception as e:
            log_err("fatal error ",e)
            traceback.print_exc()
            closeLoggers(__name__)
            return 3
    else:
        log_err("\nsyntax: fontforge -script kmn2csv.py %kmn%.kmn kmn%kmn%.csv")
        log_err("  i.e. - script Python script file,  SUN7_251.kmn kmnSUN7_251.csv")
        return 1

    log_info('done file is in',outFile.split('.')[0]+'.ods')
    closeLoggers(__name__)
   
    return 0



if __name__ == "__main__":
   
    print('name main',type(sys.argv),sys.argv)
    main(sys.argv)    