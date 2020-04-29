''' create xlsx spreadsheet then convert to ODS
    https://xlsxwriter.readthedocs.io
    https://cxn03651.github.io/write_xlsx/format.html

'''
import os
import xlsxwriter
from util import log_info, log_err, convert2ods, convert2pdf

# lang2xlsx formats and writes a spreadsheet for xlsx and ods files
def array2xlsx(ary, outFile, pdf=False):
    # https://xlsxwriter.readthedocs.io
    fxlsx = outFile.split('.')[0]+'.xlsx'
    workbook = xlsxwriter.Workbook(fxlsx)
    worksheet = workbook.add_worksheet()
    log_info('xlsx', outFile)

    col = 0
    row = 0
    print('row len', len(ary[2]))
    #populate the table
    for i in ary:
        #log_info('\nws',row,ary[i])
        worksheet.write_row(row,col, i)
        row += 1
    # format for symbol column
    s_fmt = workbook.add_format()
    s_fmt.set_font_name('SUN7_6')
    s_fmt.set_font_size(32)
    s_fmt.set_align('center')
    s_fmt.set_align('vcenter')
    s_col_width = 7.9
    
    # format for other columns
    d_fmt = workbook.add_format()
    d_fmt.set_font_size(12)
    d_fmt.set_text_wrap()
    d_fmt.set_align('left')
    d_fmt.set_align('vcenter')
    d_col_width = 25
    u_col_width = 6     #unicode column width
    
    worksheet.set_column('A:A', s_col_width, s_fmt)
    if len(ary[2]) < 4:
       worksheet.set_column('B:B', d_col_width, d_fmt) 
       worksheet.set_column('C:C', u_col_width, d_fmt)

    else:
        worksheet.set_column('B:C', d_col_width, d_fmt)
        worksheet.set_column('D:D', u_col_width, d_fmt)

    worksheet.center_vertically()
    worksheet.center_horizontally()
    
    workbook.close()
    convert2ods(fxlsx, 'dist')
    fods = outFile.split('.')[0]+'.ods'
    log_info('ODS file created',fods)
    exists = os.path.isfile(fxlsx)
    if exists:
        log_info('delete existing file',fxlsx)
        os.remove(fxlsx)
    
    if pdf:    
        # Libreoffice needs ods file to generate pdf correctly
        convert2pdf(fods)
        
    
