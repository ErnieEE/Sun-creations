
import os
import sys

import json

cfg = { 
    "filePath": "dist/",
    "version": "76",
    "alias": "EN",
    "language": "English",
    "sfdFile": "SUN7_6.sfd",
    "kmnFile": "sun7_6.kmn", 
    "trlangFile": "trlang.ods",
    "ttf": "times.ttf",
    "pwFile": "",
    "langFile": "",
    "backFont": "",
    "kmncsv": "",
    "back2doc": "",
    "compactFile": "",
    "enColumns": {"index_font": 0, "index_name": 1, "index_unicode": 2},
    "langColumns": {"index_font": 0, "index_name": 1, "index_langName": 2,
                    "index_unicode": 3},
    "eFilter": ""
    }

langParms = {\
    "Russian":"RU",\
    "Spanish":"ES",\
    "French":"FR",\
    "Portuguese":"PT",\
    "English":"EN"}


def updateCfg():
    cfg["pwFile"] = cfg["filePath"]+"pw"+cfg["version"]+"_EN.csv"
    cfg["langFile"] = cfg["filePath"]+"pw"+cfg["version"]+"_"+cfg["alias"]+".csv"
    cfg["backFont"] = cfg["filePath"]+"SUNBF"+cfg["version"]+"_"+cfg["alias"]      
    cfg["kmncsv"] = cfg["filePath"]+"kmn"+cfg["version"]+"_"+cfg["alias"]+".csv"
    cfg["back2doc"] = cfg["filePath"]+"back"+cfg["version"]+".txt"
    cfg["compactFile"] = cfg["filePath"]+"compact"+cfg["version"]+"_"+cfg["alias"]+".ods"

    if cfg["alias"] != "EN":
        cfg["langColumns"]["index_name"] = 1
        cfg["langColumns"]["index_langName"] = 2
        cfg["langColumns"]["index_unicode"] = 3
   
    else:
        cfg["langColumns"]["index_name"] = 1
        cfg["langColumns"]["index_langName"] = cfg["enColumns"]['index_name']
        cfg["langColumns"]["index_unicode"] = cfg["enColumns"]['index_unicode']

    
    
    
    
    json.dump(cfg, open('config.json', 'w'),  indent=4)
    #print('saved', cfg)
    
    
def readCfg():  
    global cfg
    cfgFile = os.path.isfile('config.json')
    if cfgFile:
        cfg = json.load(open('config.json'))
    else:
        json.dump(cfg, open('config.json', 'w'),  indent=4)
        #cfg = json.load(open('config.json'))
    return cfg
    
#updateVars()  
if __name__ == "__main__":
   
    print('name main',type(sys.argv),sys.argv)
    for a in sys.argv:
        print(a)
    #main(sys.argv)    
    
    cfgFile = os.path.isfile('config.json')
    if cfgFile:
        cfg = json.load(open('config.json'))
        cfg["sfdFile"] = sys.argv[1]
        cfg["kmnFile"] = sys.argv[2]
        cfg["version"] = sys.argv[3]
        cfg["ttf"]     = sys.argv[4]
        cfg["alias"]   = sys.argv[5]
        for x in langParms:
            if langParms[x] == cfg["alias"]:
                cfg["language"] = x
                break
        updateCfg()