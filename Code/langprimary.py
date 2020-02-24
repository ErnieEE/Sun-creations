# routine to change glyph names in font
#  https://stackoverflow.com/questions/24334747/how-to-merge-two-text-files-around-a-common-value-in-python
'''
first generate xref file:  python xplitxref.python
then generate synonmym file: python synonyms.py
invoke with:
fontforge -script filename
    filename is a the dictionary file sorted by unicoed saved as as a cvs file
    will create a file mergecsv.csv  which is dictionary.cvs with xref and synonymns
a # can be placed in front of a line to comment it out
Tkinter → tkinter
tkMessageBox → tkinter.messagebox
tkColorChooser → tkinter.colorchooser
tkFileDialog → tkinter.filedialog
tkCommonDialog → tkinter.commondialog
tkSimpleDialog → tkinter.simpledialog
tkFont → tkinter.font
Tkdnd → tkinter.dnd
ScrolledText → tkinter.scrolledtext
Tix → tkinter.tix
ttk → tkinter.ttk
I advise you to learn how to dyn
'''

import sys
import csv
#import tkinter 
#import tkinter.filedialog
#import tkinter, tkfiledialog

script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open('Log\\'+logname+".log", "w",encoding="utf-8")
 
 
def exitApp():
    sys.exit() 
    
langfile = "ru.csv"
pwfile = "pw724.csv"
langout = "langpw.csv"
ixSym = 0
ixUni = 3
ixEN = 1
ixLang = 2

#langname = ""
#languec = ""
pwname = ":"   #name from pw724.csv  english primary file
pwuec = ":"	    #uec from pw724.csv english primary file

with open(pwfile, 'r', encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        name = row[2].strip()
        uec = row[1].strip()
        pwname = pwname+':'+name
        pwuec = pwuec+':'+uec.lower()
    print('pwname',pwname)
    print('pwuec',pwuec)

fr = open(langfile, 'r', encoding='utf8')
fw = open(langout, 'w', encoding='utf8')
reader = csv.reader(fr, delimiter=',', quotechar='"')
writer = csv.writer(fw, delimiter=',', lineterminator='\n')
for row in reader:
    #print(len(row), row)
    if len(row) < 4:
        continue
    # rearrange columns for consistency  
    lnRow = []
    lnRow.append(row[ixSym].strip())
    lnRow.append(row[ixEN].strip())
    lnRow.append(row[ixUni].strip().lower())
    lnRow.append(row[ixLang].strip())
    print(lnRow[3],len(lnRow[3]), lnRow)
    if len(lnRow[3]) == 0:
        lnRow[3] = lnRow[ixEN]
    rowx = ':'+lnRow[ixEN]+':'
    print(lnRow[ixUni],rowx, rowx in pwname)
    if rowx in pwname:
        writer.writerow(lnRow)
fw.close()
fr.close()
print('done')