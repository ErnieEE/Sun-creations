'''
create SUN kmn file from SUN csv dictionary.
    i.e   fontforge -script csv2kmn.py infile.csv  version outfile.kmn

'''
import fontforge
import sys
import csv


script = sys.argv[0]
#logname = script.split('.')[0]
#sys.stdout = open('Log\\'+logname+".log", "w",encoding="utf-8")


index_uic = 0
index_name = 1
index_unicode = 3
index_lang = 2


def read_csv(fin, fout):
    csvData = []
    with open(fin, encoding='utf8', newline='') as fr:
        fw = open(fout, 'w' ,encoding='utf8', newline='')
        csvWriter = csv.writer(fw)
        data = list(csv.reader(fr))
        for i in data:
            print(i)
            uic = i[index_uic]
            enname = i[index_name]
            unicode = i[index_unicode].lower().strip()
            lname = i[index_lang].strip()
            lname1 = lname.replace(' ','_')
            #i[index_lang] = lname1
            print(lname, lname1)
            csvWriter.writerow([uic, unicode, enname, lname1])
        fw.close()
    fr.close()


    
ix = 0
for arg in sys.argv:
    print( ix,arg)
    ix = ix + 1
    
if len(sys.argv) == 3: 
    read_csv(sys.argv[1], sys.argv[2])

else:
    print("fix dictionary and rearange columns if needed.")
    print(" i.e   fontforge -script space2_.py infile.csv outfile.csv")



