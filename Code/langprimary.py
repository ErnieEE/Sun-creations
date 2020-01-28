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
sys.stdout = open(logname+".log", "w",encoding="utf-8")
 
 
def exitApp():
    sys.exit() 
    
langfile = "p.csv"
pwfile = "pw724.csv"
langout = "langpw.csv"

langname = ""
languec = ""
pwname = ":"
pwuec = ":"	

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
    row[0] = row[0].strip()
    row[1] = row[1].strip()
    row[2] = row[2].strip()
    row[3] = row[3].strip()

    row1 = ':'+row[1]+':'
    if row1 in pwname:
        writer.writerow(row)
fw.close()
fr.close()
''''
with open(out, 'w') as fout:
    print('Not in '+pwfile+'\n')
    pwlist = pwname.split(':')
    for name in pwlist:
        if name not in langname:
            print('o notin langname',name)

    ueclist = pwuec.split(':')        
    for uec in ueclist:
        if uec not in languec:
            print('o notin languec',uec)
        
    print('\nNot in '+langfile+'\n')
    langlist = langname.split(':')
    for name in langlist:
        if name not in pwname:
            print('n not in pwname',name)
        else:
            wr
          
            
    ueclist = languec.split(':')
    for uec in ueclist:
         if uec not in pwuec:
            print('n not in pwuec',uec)
'''

