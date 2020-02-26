# create synonym list and merge with xref file
# 

import fontforge
import os
import sys
import csv
import logging


script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open('Log\\'+logname+".log", "w",encoding="utf-8")
 
#priData = []
#xrefData = []
#synData = {}    # dictionary file of synonymns {key=unicode, value= synonyms}
xuniCol = 2     # unicode column in xref
xnameCol = 1    # name column in xref 
xrefCol = 3     # xref column in xref
xglyphCol = 0     # fontforge glyph
puniCol = 1     # unicode column in primary
pnameCol = 2    # name column in primary

def getUnicode(str):
    a = chr(int(str,16)).encode('utf-8')
    #print('getunicode hex:',str,' unicode:', a.hex(), a.decode('utf-8'))
    return a.decode('utf-8')



def synonyms(xref):
    pSort = sorted(xref, key=lambda item: item[xuniCol]) # sort by unicode column
    #pSort = sorted(xref, key=lambda x: x[xuniCol].casefold())  
    os.remove("synonyms.csv")
    synFile = open("synonyms.csv", "x")   # create synonymn text file
    prevuec = '***'
    prevname = '***'
    count = 0
    synArry = {}
    istr = ""
    synStr = ""
    for line in pSort:
        if len(line) > 3:
            uec = line[xuniCol].strip().lower()
            name = line[xnameCol].strip()
            if uec == prevuec:
                count = count+1
                if count > 1:
                    #print(' ', name, end='')
                    istr = ' '+name
                    synStr = synStr + istr
                    synFile.write(istr)
                else:	
                    #print('\n',uec, name, prevname , end='')
                    istr = uec+' '+name+' '+prevname
                    synStr = istr
                    strn = '\n'+istr
                    synFile.write(strn)
            else:
                count = 0
                if len(synStr) > 0:
                    #print('synStr',len(synStr), synStr)
                    synArry[synStr[:4]] = synStr[5:].strip()
                synStr = ""

        prevuec = uec
        prevname = name
        
    synFile.close()
    return synArry

def arry2Obj(arry):
    xd = {}
    for i in arry:
        #glyph = i[xglyphCol]
        #unicode = i[xuniCol]
        name = i[xnameCol]
        xrefd = i[xrefCol]
        xd[name] = xrefd
    return xd
    
# merge xref and synonyms  p=primary, x = xref, s = synonymn    
def mergeXrefSyn(p,x, s):
    print('merge')
    data = []
    xd = arry2Obj(x)
    for key in p:
        word = p[key]
        item = []
        if s.get(key) != None:
            synlist = s[key]
            item.append(key)
            item.append(word)
            item.append(s[key])
        else:
            item.append(key)
            item.append(word)
            item.append("")
 
        if xd.get(word) != None:
            item.append(xd[word])
        else:
            item.append("")
            
        data.append(item)  
    return(data)

def read_syn(f):
    with open(f, encoding='utf8', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    return data
        
def writexref(outfile, ddata):
    print('wrtexref')
    with open(outfile, 'w', encoding='utf8') as f:
        for row in ddata:
            name = row[1]
            uec = row[0].lower()
            syn = row[2]
            xref = row[3]
            if "," in xref:
                xref = '"'+xref+'"'
            unicode = getUnicode(uec)
            f.write(unicode+','+name+','+syn+','+uec+','+xref+'\n')        
 
def read_xref(f):
    with open(f, encoding='utf8', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    return data

    
def read_pri(f):
    pd = {}
    with open(f, encoding='utf8', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for i in data:
            symbol = i[xglyphCol]
            unicode = i[puniCol]
            name = i[pnameCol]
            pd[unicode] = name
    return pd

 
ix = 0
print(len(sys.argv))
for arg in sys.argv:
    print(ix,arg)
    ix=ix+1
 
if len(sys.argv) > 3: 
    priData = read_pri(sys.argv[1])
    xrefData = read_xref(sys.argv[2])
    outFile = sys.argv[3]
    synData = synonyms(xrefData)
    mergeData = mergeXrefSyn(priData, xrefData, synData)
    writexref(outFile, mergeData)
else:
    print("\nsyntax: fontforge -script synxref.py primaryCSV  xrefCSV")
    print("Creates a synonym file and a merged xref and synonym file")

print ('\n*** done ****')


