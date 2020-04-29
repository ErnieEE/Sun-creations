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
    
for arg in sys.argv:
    print( len(sys.argv),arg)
#pw%ver%.csv %lang%.csv langpw.csv
if len(sys.argv) > 2: 
    pwfile  = sys.argv[1]
    langfile = sys.argv[2]
    langout = "langpw.csv"

else:
    print("\n  SYNTAX: fontforge -quiet -script langprimary.py pw%ver%.csv %lang%.csv ") 
    print("Creates 'langpw.csv' as a list of all primary words in language")
    sys.exit()    
    
    
#langfile = "es.csv"
#pwfile = "pw724.csv"
#langout = "langpw.csv"
# lang file xx.csv order
pwSym = 0
pwUni = 1
pwName = 2 

langSym = 0
langUni = 1
enName =  2
langName = 3

#enName = ""
#languec = ""
pwname = ":"   #name from pw724.csv  english primary file
pwuec = ":"	   #uec from pw724.csv english primary file

with open(pwfile, 'r', encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        name = row[pwName].strip().strip('"').strip("'")
        uec = row[pwUni].strip().strip('"').strip('"').lower()
        pwname = pwname+':'+name
        pwuec = pwuec+':'+uec.lower()
    print('pwname',pwname)
    print('pwuec',pwuec)

fr = open(langfile, 'r', encoding='utf8')
fw = open(langout, 'w', encoding='utf8')
reader = csv.reader(fr, delimiter=',', quotechar='"')
writer = csv.writer(fw, delimiter=',', lineterminator='\n')
misscount = 0
for row in reader:
    #print(len(row), row)
    if len(row) < 4:
        continue
    # rearrange columns for consistency  
    # data in lang file
    lnRow = []
    sym = row[langSym].strip().strip('"').strip("'")
    name = row[enName].strip().strip('"').strip("'")
    uni = row[langUni].strip().strip('"').strip("'").lower()
    lang = row[langName].strip().strip('"').strip("'")
    lnRow.append(sym)
    lnRow.append(name)
    lnRow.append(uni)
    lnRow.append(lang)
    print(lnRow)
    #print(lang,len(lang), uni, name)
    if len(lang) == 0:
        print('lang name len 0', name)
        lnRow[ixLang] = name
    rown = ':'+name+':'
    rowu = ':'+uni+':'
    print(lang, rown, rowu, rown in pwname, rowu in pwuec)
    # compare lang file with english
    if rown in pwname and rowu in pwuec:
        print('inboth',rown, rowu)
        writer.writerow(lnRow)
        pwuec = pwuec.replace(uni,"")  #remove incase duplicate in language file
        pwname = pwname.replace(name,"")
    else:
        misscount = misscount+1
        print(misscount,'Check for unicode', rowu, rowu in pwuec)
        if rowu in pwuec:
            print('inUnec')
            #lnRow[0] = uni
            writer.writerow(lnRow)
            pwuec = pwuec.replace(uni,"")  #replace all occurances of substring
print('pwname again')
print(pwname)
fw.close()
fr.close()
print('done')