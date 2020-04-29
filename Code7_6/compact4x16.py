"""
 https://xlsxwriter.readthedocs.io
 https://ask.libreoffice.org/en/question/75384/is-it-possible-to-format-a-libreoffice-spreadsheet-using-a-shell-script/
 Creates a condensed view of the dictionary  with the unicode and name in same column
rem open command prom[t as admin
rem cd to fontforgebuilds dir
rem execute fontforge-console
rem execute ffpython -m pip install --upgrade pip --force-reinstall
rem execute pip install xlsxwriter

   fontforge -script imageref.py infile outfile')
     Example: fontforge -script genesis.csv genout.csv\n')

This program automatically resizes the spreadsheet formats to make 
into a pdf 

"""

import sys
import os
import csv
#import json
import xlsxwriter
import traceback
from util import log_info, log_err, new_logger, closeLoggers, convert2ods, convert2pdf
from bfConfig import readCfg 

cfg = readCfg()
#print('cfg',cfg)
#print('cfg',cfg["alias"], cfg["langColumns"])

IMAGEPOS = cfg["enColumns"]["index_font"]
LANGNAMEPOS = cfg["langColumns"]["index_langName"]
UECPOS = cfg["langColumns"]["index_unicode"]
ENNAMEPOS = cfg["langColumns"]["index_name"]

COLUMNS = 4
ROWSPERPAGE = 16
debug = False

#symbol unicode name
def read_csv_data(path):
    try:
        f = open(path, 'r', encoding="utf-8")
        csvReader = csv.reader(f, delimiter=',', quotechar='"')
        # Assume no column headers
        data_lines = []
        #make sure data us sorted by name
        name_sort = sorted(csvReader, key=lambda x: x[LANGNAMEPOS].lower())
        count = 0
        for row in name_sort:
            #log_info(row, type(row[2]), type(row[1]))
            if debug:
                count += 1
                row[2]=str(count)+' '+row[2]
                if count > 70:
                    break
            
            data_lines.append(row)
            if debug:
                log_info(row)
        return data_lines		
    except Exception as e:
        log_err('exception',e)
        traceback.print_exc()
        return ""

def createCell(row):
    name = row[LANGNAMEPOS]
    uec = row[UECPOS]
    image = row[IMAGEPOS]
    line = name+'\n('+uec+')'    #,'+syn;
    return line
    
COLUMNS = 4

COLUMNS = 4
ROWSPERPAGE = 16
NOPERPAGE = COLUMNS*ROWSPERPAGE

def csv2_4x16(csvArray):
    dlen = len(csvArray)
    rows = []
    cnt = 0
    for x in range(0, len(csvArray), 64):
        log_info(x,'----')
        #line = []
        m = min(x+16, len(csvArray))
        for y in range(x, m):
            line=[]
            if y < dlen:
                line.append(csvArray[y][0])
                line.append(createCell(csvArray[y]))
            if y+16 < dlen:
                line.append(csvArray[y+16][0])
                line.append(createCell(csvArray[y+16]))
            if y+32 < dlen:
                line.append(csvArray[y+32][0])
                line.append(createCell(csvArray[y+32]))
            if y+48 < dlen:
                line.append(csvArray[y+48][0])
                line.append(createCell(csvArray[y+48]))
            log_info(' ',line)
            rows.append(line)
    #log_info('rows',rows)
    #for x in rows:
    #   log_info('---',x)
    return rows

def arry2xlsx(ary, outFile):
    # https://xlsxwriter.readthedocs.io
    fout = outFile.split('.')[0]
    fxlsx = fout+'.xlsx'
    workbook = xlsxwriter.Workbook(fxlsx)
    worksheet = workbook.add_worksheet()
    log_info('arry2xlsx', fxlsx)

    col = 0
    #populate the table
    for row, data in enumerate(ary):
        #log_info('\nws',row,col,data)
        worksheet.write_row(row,col, data)

    
    s_fmt = workbook.add_format()
    s_fmt.set_font_name('SUN7_6')
    s_fmt.set_font_size(32)
    #s_fmt.set_font_size(12)
    s_fmt.set_align('center')
    s_fmt.set_align('vcenter')
    s_col_width = 7.9
    
    
    d_fmt = workbook.add_format()
    d_fmt.set_font_size(12)
    d_fmt.set_text_wrap()
    d_fmt.set_align('left')
    d_fmt.set_align('vcenter')
    d_col_width = 14.1
    
    worksheet.set_column('A:A', s_col_width, s_fmt)
    worksheet.set_column('C:C', s_col_width, s_fmt)
    worksheet.set_column('E:E', s_col_width, s_fmt)
    worksheet.set_column('G:G', s_col_width, s_fmt)
    
    worksheet.set_column('B:B', d_col_width, d_fmt)
    worksheet.set_column('D:D', d_col_width, d_fmt)
    worksheet.set_column('F:F', d_col_width, d_fmt)
    worksheet.set_column('H:H', d_col_width, d_fmt)

    # create page breaks so data lines up with sort
    pg_brk = []
    for i in range(0, len(ary), 16):
        pg_brk.append(i)
    
    worksheet.set_h_pagebreaks(pg_brk)
    worksheet.set_margins(0.5,0.5)
    worksheet.center_vertically()
    worksheet.center_horizontally()
    
    workbook.close()
    # create pdf
    # Libreoffice needs ods file to generate pdf 
    # does not work properly xlsx->pdf
    convert2ods(fxlsx, 'dist')
    convert2pdf(fout+'.ods','dist')
    exists = os.path.isfile(fxlsx)
    if exists:
        log_info('delete existing file',fxlsx)
        os.remove(fxlsx)
    
    
def main(*ffargs):
    new_logger("compact4x16")    
    
    args = []
    for a in ffargs[0]:
        log_info( a)
        args.append(a)

    if len(args) ==3: 
        csv_file = args[1]
        outFile = args[2]
    else:
        log_err('\n>>  fontforge -script imageref.py infile outfile')
        log_err('>>  Example: fontforge -script genesis.csv genout.csv\n')
        log_err('Creates a condensed view of the dictionary  with the unicode')
        log_err('and name in same cell.');
        return 1
  

    csv_data = read_csv_data(csv_file)
    if csv_data:
        #name_sort = sorted(csv_data, key=lambda x: x[LANGNAMEPOS].lower())
        ary =csv2_4x16(csv_data)
        arry2xlsx(ary, outFile)
        log_info('\n** done ** files are in',outFile)
        rc = 0
    else:   
        rc = 1
    closeLoggers(__name__)
    return rc


if __name__ == "__main__":
   
    print('name main',type(sys.argv),sys.argv)
    main(sys.argv)    