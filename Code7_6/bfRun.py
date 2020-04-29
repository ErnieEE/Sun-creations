#
# https://likegeeks.com/python-gui-examples-tkinter-tutorial/
#
'''
set sfd="SUN7_251 Font_0219.sfd"
set ver=7251
set font=times
set alias=EN
set language=english



'''
import os
import subprocess
import fontforge
import time
from util import runTime, log_info, log_err
from bfConfig import *
from sfd2csv import main as sfd2csvMain
from svg2Font import main as svg2FontMain
from csv2svg import main as csv2svgMain
from kmn2csv import main as kmn2csvMain
from back2doc import main as back2docMain
from compact4x16 import main as compactMain

RUNNING = False
ABORT = False

cfg = readCfg()
 
def bfExit(e):
    #log_info(e)
    if RUNNING:
        ABORT = True
        errBox.insert(END, "ABORT hit")
        errBox.see(END)
        errBox.update_idletasks() 
    else:  
        quit()

def langClicked(v):
    sv = v.get()
    sv = sv.capitalize()
    bf.alias.set(cg.langParms[sv])
    bf.language.set(sv)
    cg.cfg["language"] = sv
    cg.cfg["alias"] = cg.langParms[sv]
    cg.updateVars()

 
    
def aliasClicked(v):
    a = v.get().upper()
    #lookup = {value: key for key, value in cg.langParms}
    found = False
    for k in cg.langParms:
        value = cg.langParms[k]
        if value == a:
            found = True
            break
    log_info(k,value, found)
    if found:
        bf.alias.set(value)
        bf.language.set(k)
        cg.cfg["language"] = k
        cg.cfg["alias"] = cg.langParms[value]
        cg.updateVars(root)



'''
row = 6
canvas = Canvas(gui.ctr_left, width = 200, height = 300)      
canvas.grid(column=0, row=row, columnspan=6, sticky=NSEW)  
'''

#
#bfcmd = {"sfd2csv": ['sfd2csv.py', bf.sfdFile, bf.langFile.get()],\
#        "kmn2csv": ['kmn2csv.py', bf.kmnFile, bf.kmncsv.get()]\
#   }
#bfcmd = ['x'+bf.langFile.get()+'x']

def xffPath():
    paths = os.environ['PATH'].split(';')
    for i in paths:
        log_info(i)
        if 'FontForgeBuilds' in i:
            fp = i
            break
    return fp+'\\fontforge.bat'


def sfd2csv():
    log_info('sfd2csv')
    btnDisable('sfd2csv')
    log_info('pwfile',cfg["pwFile"])
    cmd = ['sfd2csv.py', cfg["sfdFile"], cfg["pwFile"]]
    #cmd /c fontforge -quiet -script sfd2csv.py %sfd% dist/pw%ver%_%alias%.csv

    rc = sfd2csvMain(cmd)
    btnEnable()
    log_info('return sfd2csv',rc)
    return rc
def langPri(): 
    log_info('lan')
    btnDisable('langPri')
    rc = cmdPath(['langprimary.py', cfg["pwFile"], cfg["trlangFile"], cfg["alias"]])
    btnEnable()
    log_info('return langpri',rc)
    return rc    
def kmn2csv():
    log_info('kmn')
    btnDisable('kmn2csv')
    cmd = ['kmn2csv.py', cfg["kmnFile"], cfg["kmncsv"]]
    rc = kmn2csvMain(cmd)
    btnEnable()
    log_info('return kmn2csv staus = ',rc)
    return rc
def csv2svg():
    log_info('svg')
    btnDisable('csv2svg')
    #rc = cmdPath(['csv2svg.py', bf.langFile.get(), bf.alias.get(), bf.ttf, efltr.get()])
    cmd = ['csv2svg.py',
            cfg["langFile"],
            cfg["ttf"], 
            cfg["eFilter"]]
    rc = csv2svgMain(cmd)
    btnEnable()
    log_info('return csv2svg',rc)
    return rc

def svg2Font():
    log_info('font')
    btnDisable('svg2Font')
    
    cmd = ['svg2Font.py', cfg["pwFile"], cfg["ttf"], cfg["alias"],
             cfg["backFont"], cfg["eFilter"]]
    rc = svg2FontMain(cmd) 
    btnEnable()
    log_info('return svg2font status =',rc)
    return rc    

def back2doc():
    log_info('back2doc')
    btnDisable('back2doc')
    cmd = ['back2doc.py', cfg["pwFile"], cfg["back2doc"]]
    log_info(cmd)
    rc = back2docMain(cmd)
    btnEnable()
    log_info('return back2font',rc)
    return rc
    
def bfCompact():
    log_info('bfCompact')
    btnDisable('compact4x16')
    cmd = ['compact4x16.py', cfg["pwFile"], cfg["compactFile"]]
    log_info(cmd)
    rc = compactMain(cmd)
    btnEnable()
    log_info('return bfCompact',rc)
    return rc
    
cmdBtns = {}
cmdList = [sfd2csv, kmn2csv, csv2svg, svg2Font, back2doc, bfCompact]

def doall():
    log_info("doall")
    status = ""
    for i in cmdList:
        #log_info(i)
        st = i()
        status = status+' '+str(st) 
        if st != 0:
            break
        time.sleep(1.0)   # allow time for logging and display to catch up
     
    if st != 0:
        stmsg = str(i)+" failed Status = "+str(st)
        log_err('doall',stmsg)
      
    else:
        stmsg = "All functions finished  status "+status
        log_info('doall',stmsg)


def btnDisable(btn):
    #log_info("btn disable")
    for c in cmdBtns:
        cmdBtns[c]['state'] = 'disable'
    cmdBtns[btn].configure(state = 'normal')
    #log_info("return btn disable")


def btnEnable():
    #log_info("btn enable")
    for c in cmdBtns:
        cmdBtns[c]['state'] = 'normal'
        #log_info(c)
    #log_info("return btnenable")
