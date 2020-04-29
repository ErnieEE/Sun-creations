#  2 letter language codes
# https://www.sitepoint.com/iso-2-letter-language-codes/


import configparser

'''
fontName = "Arial"                 # font used to generate backfont words
imagedir = "svg/"
char_ascent = "bdfhijklt"      # character with ascending stems
ES_char_ascent = "bdfhijkltíéóñúá"      # character with ascending stems    reír  por_qué cómo año según maná
char_descent = "_gjpqy"      # characters with descending stems
font_xheight = 1062
font_ascender = -431            #  length of ascenders in font
font_descender = 1491           # length of descenders in font
backfont_xheight = 200
font_name = "Times"

# index in csv file column number of font, name, unicode         
index_font = 0
index_name = 1                    # 1 for english 3 for other languages 
index_unicode = 2
section = "EN"
'''
# https://tutswiki.com/read-write-config-files-in-python/
config_object = configparser.ConfigParser()
'''
[LANGINFO]
    english = {'char_ascent': 'bdfhijklt','char_descent': '_gjpqy','index_name': '0','index_unicode': '1','alias': 'EN'}
    spanish = {'char_ascent': 'bdfhijkltíéóñúá','char_descent': '_gjpqy','index_name': '0','index_unicode': '1','alias': 'ES'}

[FONTMETRICS]
    arial.ttf = {'file': 'arial.ttf','xheight': '1062','descender': '-431','ascender': '1491'}
    times.ttf = {'file': 'times.ttf','xheight': '916.0','ascender': '1420','descender': '-442'}
    fonrtame = {'file': 'fodntNrame','xheight': '1111','ascender': '222','descender': '533'}
'''


config_object["LANGINFO"] = {
    # language: font, char_ascent char_descent index_name index_unicode
    "ENGLISH": {"alias": "EN", "char_ascent": "bdfhijklt", "char_descent": "_gjpqy", "index_name": "0", "index_unicode": "1"},
    "SPANISH": {"alias": "ES", "char_ascent": "bdfhijkltíéóñúá", "char_descent": "_gjpqy", "index_name": "0", "index_unicode": "1"}
}

config_object["FONTMETRICS"] = {
    #"fontmetrics": "fontfile, xheight, descender, ascender"
    #"times.ttf": {"file":"times.ttf", "xheight": "916",  "descender": "-442", "ascender": "1420"},
    "arial.ttf": {"file":"arial.ttf", "xheight": "1062", "descender": "-431", "ascender": "1491"}
}

def writeConfig(dict):
    # https://tutswiki.com/read-write-config-files-in-python/
    #Write the above sections to config.ini file
    with open('config.ini', 'w') as conf:
        dict.write(conf)
            
def readConfig():
    #Read config.ini file
    config_object.read("config.ini")
    return(as_dict(config_object))
    

def getSections():
    config_object.read("config.ini")
    #print("sections ",config_object.sections())
    return config_object.sections()

def getObjects(section, value = ""):
    config_object.read("config.ini")
    sct = config_object[section.upper()] 
    if value:
        for o in sct:
            if o == value:
                a = sct[o].replace("{","").replace("}","").replace("'","").replace(" ","")
                a = a.split(',')
                d = dict(s.split(':') for s in a)
                return d

    else:
        sct = config_object[section]
        print(sct)
        return ""
 
def updateKey(config,section,obj,key,value): 
    try:
        r = dict[section.upper()][obj.lower()]
        r[key] = value
        print(key,value, "updated")
    except Exception as ex:
        print("Update key error",ex.args)
        sys.exit(1)
 
def addKey(config, section,obj,key,value):
    r = dict[section.upper()][obj.lower()]
    r[key] = value
    print(key,value, "added")
    
def delKey(config,section,obj,key):
    try:
        r = dict[section.upper()][obj.lower()]
        del r[key]   
        print(key,"deleted")
    except Exception as ex:
        print("Delete key error",ex.args)
        sys.exit(1)

 
def as_dict(config):
    """ https://stackoverflow.com/questions/1773793/convert-configparser-items-to-dictionary
    Converts a ConfigParser object into a dictionary.
    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """
    the_dict = {}
    vdict = {}
    for section in config.sections():
        the_dict[section] = {}
        for key, val in config.items(section):
            #print('va;',val)
            v = val.replace("{","").replace("}","").replace("'","").replace(" ","").strip().rstrip(',')
            #print('v',v)
            kv = v.split(',')
            #print('kv',kv)
            vdict = {}
            d = dict(s.split(':') for s in kv)
            the_dict[section][key] = d
            #print(key,v)
    #print('thedict',the_dict)
    return the_dict   
   
def printdict(dict):   
    for d in dict:
        print('section',d)
        for e in dict[d]:
            print('  object',e)
            for f in dict[d][e]:
                print('     field ',f, dict[d][e][f])
                
def savedict(dict): 
    parser = configparser.ConfigParser()
    for d in dict:
        parser.add_section(d)
        for e in dict[d]:
            #print('  obj ',e)
            str = "{"
            for f in dict[d][e]:
                #print('     obj',f, dict[d][e][f]) 
                str = str+"'"+f+"': '"+dict[d][e][f]
                str = str+"',"
            str = str.strip(',')+"}"
            parser.set(d, e, str)
            print('save',str)
            
    #with open('config.ini', 'w') as f:
    #    parser.write(f)    
    writeConfig(parser)

    
debug = 0
if debug:
  
    #writeConfig()
    dict = readConfig()
    #updateConfig()
 
    #delKey(dict,"LANGINFO", "spanish", "font")
    #addKey(dict,"langinfo","spanish","alias","ES") 
    #addKey(dict,"langinfo","english","alias","EN")
    updateKey(dict,"langinfo","spanish","index_name", str(2))
    updateKey(dict,"langinfo","spanish","index_unicode",str(1))
    printdict(dict)
    
    savedict(dict)
