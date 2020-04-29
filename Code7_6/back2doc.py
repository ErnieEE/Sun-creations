# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import fontforge
import sys
import csv
import traceback
from util import log_info, log_err, getUnicode, new_logger, closeLoggers
from bfConfig import readCfg  
 
def read_csv(namelist, outfile):
    try:
        #cfg = json.load(open('config.json'))
        cfg = readCfg()
        ixu = cfg["langColumns"]["index_unicode"]
        log_info('read_csv',namelist,outfile)
        fr = open(namelist, 'r', encoding='utf8')
        fw = open(outfile, 'w' , encoding='utf8')
        csvReader = csv.reader(fr, delimiter=',')
        for row in csvReader:
            log_info(row);
            uic = row[ixu].strip()
            if uic != "":
                unicode = getUnicode(uic)
                fw.write(unicode)
        fr.close
        fw.close()
        return 0
    except Exception as e:
        log_err('exception',e)
        traceback.print_exc()
        return(1)
 
def main(*ffargs):  
    new_logger("back2doc")    
    args = []
    for a in ffargs[0]:
        log_info(a)
        args.append(a)


 
    if len(args) == 3: 
        infile = args[1]
        outfile = args[2]
    else:
        log_err("\nsyntax: fontforge -script back2doc.py output.txt")
        log_err("\nCreates a backfont text file for verification of word alignment")
        return 1

    rc = read_csv(infile, outfile)
    if rc == 0:
        log_info("Done!  The backdoc file is in", outfile)
        
    closeLoggers(__name__)
    return rc


if __name__ == "__main__":
   
    print('name main',type(sys.argv),sys.argv)
    main(sys.argv)  