'''
create SUN kmn file from SUN csv dictionary.
    i.e   fontforge -script csv2kmn.py infile.csv  version outfile.kmn

'''
import fontforge
import sys
import csv


script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open('Log\\'+logname+".log", "w",encoding="utf-8")


index_font = 0
index_name = 2
index_unicode = 1
index_lang = 3


def get_header(name):
    print('get_header', name)
    hdr = "store(&VERSION) '9.0' U+0079\n"
    hdr = hdr + "store(&TARGETS) 'any windows macosx linux web iphone ipad androidphone androidtablet mobile desktop tablet'\n"
    hdr = hdr + "store(&KEYBOARDVERSION) '090023'\n"
    hdr = hdr + "store(&LAYOUTFILE) 'Sun2-layout.js'\n"
    hdr = hdr + "store(&NAME) '"+name+"'\n"
    hdr = hdr + "begin Unicode > use(main)\n"
    hdr = hdr + "\ngroup(main) using keys"
    hdr = hdr + "\n\n"
    return hdr
    
def build_row(name, unicode):  
    #   'Aaron' + ' ' > U+Eb0d
    row = "'"+name+"' + ' ' > U+"+unicode.lower()
    return row
    
def read_csv(f):
    csvData = []
    with open(f, encoding='utf8', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for i in data:
            print(i)
            unicode = i[index_unicode].lower().strip()
            name = i[index_lang].strip()
            if unicode == 'e37e':
                name = '.'
            if unicode == 'e390':
                name = '*'
                csvData.append(build_row(name, unicode)) 
                name = 'pos'
            if unicode == 'ed11':
                name = 'pn'
            csvData.append(build_row(name, unicode)) 
    return csvData


# parse kmn file and generate csv file for documentation
def write_kmn(hdr, data, outfile):
    fw = open(outfile, 'w')
    fw.write(hdr)
    for i  in data:
        print('kmn',i)
        wstr = i+'\n'
        fw.write(wstr)
        

    fw.close()
    
ix = 0
for arg in sys.argv:
    print( ix,arg)
    ix = ix + 1
    
if len(sys.argv) > 3: 
    csvData = read_csv(sys.argv[1])
    version = sys.argv[2]
    language = sys.argv[3]
    name = "sun"+version+"_"+language
    hdr = get_header(name)
    print(hdr)
    outfile = "sun"+version+"_"+language+".kmn"
    kmnout = write_kmn(hdr, csvData, outfile)
else:
    print("Create SUN kmn file from SUN csv dictionary.")
    print(" i.e   fontforge -script csv2kmn.py infile.csv version language")



