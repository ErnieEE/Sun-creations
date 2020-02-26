# compare kmn file and sfd file looking for missing or changed items
# kmn file contains both primary and synonyms. 
# log file contains miscompares

import sys
import csv

def exitApp():
    sys.exit() 
script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open(logname+".log", "w",encoding="utf-8")

kmnfile = "kmnSUN7_24.csv"
pwfile = "pw724.csv"

kmnname = ""
kmnuec = ""
kmn_uec = {}
kmn_name = {}
pw_uec = {}
pw_name = {}

with open(kmnfile, 'r', encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        name = row[1].strip()
        uec = row[2].strip().lower()
        kmnname = kmnname+':'+name
        kmnuec = kmnuec+':'+uec
        kmn_uec[name] = uec
        kmn_name[uec] = name
    #print('kmnname',kmnname)
    #print('kmnuec',kmnuec)

		
pwname = ""
pwuec = ""	

with open(pwfile, 'r', encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        name = row[2].strip()
        uec = row[1].strip().lower()
        pwname = pwname+':'+name
        pwuec = pwuec+':'+uec
        pw_uec[name] = uec
        pw_name[uec] = name
    #print('pwname',pwname)
    #print('pwuec',pwuec)

out = "cmp.csv"


with open(out, 'w') as fout:
    '''
    print('Not in '+pwfile+'\n')
    pwlist = pwname.split(':')
    for name in pwlist:
        if name not in kmnname:
            print('o notin kmnname',name)

    ueclist = pwuec.split(':')        
    for uec in ueclist:
        if uec not in kmnuec:
            print('o notin kmnuec',uec)
        
    print('\nNot in '+kmnfile+'\n')
    kmnlist = kmnname.split(':')
    for name in kmnlist:
         if name not in pwname:
            print('n not in pwname',name)
            
    ueclist = kmnuec.split(':')
    for uec in ueclist:
         if uec not in pwuec:
            print('n not in pwuec',uec)
    ''' 
    print('compare names')
    for uec in pw_name:
        name = pw_name[uec]
        #print(uec, name, '****', kmn_name.get(uec),kmn_uec.get(name))
        if kmn_uec.get(name) == None:
            print('Misscompare', uec, name, 'not in', kmn_name.get(uec))

        #if uec not in kmn_uec:
        #    print(uec, name, 'not in kmn file kmn contains',kmn_name[uec])
    print('\ncompare uec')
    for name in pw_uec:
        uec = pw_uec[name]
        #print(un, '***', kmn_uec[un])
        if kmn_name.get(uec) == None:
            print('Misscompare',uec, name, 'not in', kmn_name.get(uec),kmn_uec.get(name))    

