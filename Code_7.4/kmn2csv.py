# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import fontforge
import sys
import csv
#import logging

script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open('Log\\'+logname+".log", "w",encoding="utf-8")
#file_handler = logging.FileHandler(filename=logname+'.log')
#stdout_handler = logging.StreamHandler(sys.stdout)
#handlers = [file_handler, stdout_handler]
'''
logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('LOGGER_NAME')
'''
def getUnicode(str):
    #print('getunicode', str)
    a = chr(int(str,16)).encode('utf-8')
    print('getunicode hex:'+str+' unicode:'+ a.hex()+' '+a.decode('utf-8'))
    return a.decode('utf-8')

index_other = 0
index_name = 1
index_unicode = 2

   
# parse kmn file and generate csv file for documentation
def read_kmn(namelist, outfile):

    fr = open(namelist, 'r')
    fw = open(outfile, 'w' ,encoding='utf8')
    csvReader = csv.reader(fr, delimiter='+')
    csvWriter = csv.writer(fw, delimiter=',', lineterminator='\n')
    for row in csvReader:
        l = len(row)
        if l == 3:
            if '>'  in row[1]:
                csvrow = []
                #print(row)
                uic = row[2].strip().strip('\"').strip("\'").lower()
                unicode = getUnicode(uic)
                csvrow.append(unicode)
                csvrow.append(row[0].strip().strip('\"').strip("\'"))
                csvrow.append(uic)
                csvWriter.writerow(csvrow)

    fr.close()
    fw.close()
    
if len(sys.argv) > 1: 
    namelist = sys.argv[1]
    out = sys.argv[2]
    read_kmn(namelist, out)
else:
    namelist = str(input("enter kmn file name as input"))
    out = str(input("enter csv output file name"))
    print("\nsyntax: fontforge -script kmn2csv.py %kmn%.kmn kmn%kmn%.csv")
    print("  i.e. - script Python script file,  SUN7_251.kmn kmnSUN7_251.csv")
    sys.exit(1)

print('done')
print (sys.version)


