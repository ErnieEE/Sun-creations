#
# https://likegeeks.com/python-gui-examples-tkinter-tutorial/
# https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid
#

from tkinter import *
#from tkinter import tix
from tkinter import filedialog
from tkinter import scrolledtext
from contextlib import redirect_stdout, redirect_stderr

from bfRun import *
from bfConfig import *

root = Tk()

root.title("SUN Font Utility")
root.resizable(width=TRUE, height=TRUE)
root.geometry('{}x{}+{}+{}'.format(760, 450, 50, 50))

class  bfClass():
    filePath = "dist/"
    version = StringVar()
    alias = StringVar()
    language = StringVar()
    sfdFile = ""
    kmnFile = "" 
    trlangFile = ""
    ttf = "times.ttf"
    pwFile = StringVar()
    langFile = StringVar()
    backFont = StringVar()
    kmncsv = StringVar()
    back2doc = StringVar()
    compactFile = StringVar()
    # index_langName -> changes to 3 if non English dictionary
    #enColumns = {"index_font": 0, "index_name": 1, "index_unicode": 2}
    #langColumns = {"index_font": 0, "index_name": 1, "index_langName": 2, "index_unicode": 3}
    testMode = 0


def updateVars():
    updateCfg()
    bfClass.pwFile.set(cfg["pwFile"])
    bfClass.langFile.set(cfg["langFile"])     
    bfClass.backFont.set(cfg["backFont"])
    bfClass.kmncsv.set(cfg["kmncsv"])
    bfClass.back2doc.set(cfg["back2doc"])
    bfClass.compactFile.set(cfg["compactFile"])
    
    bfClass.ttf = os.path.basename(cfg["ttf"])
    ttfName = os.path.basename(cfg["ttf"])
    ttf.delete(0, END)
    ttf.insert(0, ttfName)
    
    bfClass.sfdFile = os.path.basename(cfg["sfdFile"])
    sfdName = os.path.basename(cfg["sfdFile"])
    sfd.delete(0, END)
    sfd.insert(0, sfdName)
    
    bfClass.kmnFile = os.path.basename(cfg["kmnFile"])
    kmnName = os.path.basename(cfg["kmnFile"])
    kmn.delete(0, END)
    kmn.insert(0, kmnName)
    
    bfClass.trlangFile = os.path.basename(cfg["trlangFile"])
    trlName = os.path.basename(cfg["trlangFile"])
    trl.delete(0, END)
    trl.insert(0, trlName)
    
class TextIO:
    def __init__(self, text):
        self.text = text
    def write(self, msg):
        self.text.update_idletasks()
        self.text.insert(END, msg)
        self.text.see(END)
    def flush(self):
        pass 

def versionClicked(v):
    sv = v.get()
    b = sv
    log_info(b, bf.version)
    #bf.pwFile.set('pw'+bf.version.get()+'_'+bf.alias.get()+'.csv')
    cg.cfg["version"] = sv
    cg.updateVars()
    

def efltrClicked(e):
    cfg["eFilter"] = efltr.get()
    #log_info("eFilter", cfg["eFilter"])
    updateCfg()
        
    
def ttfClicked(e):
    cgf["ttf"] = filedialog.askopenfilename(filetypes = (("Text files","*.ttf"),("all files","*.*")))
    #ttfName = os.path.basename(cfg["ttf"])
    #ttf.delete(0, END)
    #ttf.insert(0, ttfName)
    updateVars()
 
def sfdClicked(e):
    cfg["sfdFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.sfd"),("all files","*.*")))
    #sfdName = os.path.basename(cfg["sfdFile"])
    #sfd.delete(0, END)
    #sfd.insert(0, sfdName)
    #cg.cfg["sfdFile"] = bf.sfdFile
    updateVars()
    
def kmnClicked(e):
    cfg["kmnFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.kmn"),("all files","*.*")))
    #kmnName = os.path.basename(cfg["kmnFile"])
    #kmn.delete(0, END)
    #kmn.insert(0, kmnName)
    #cg.cfg["kmnFile"] = kmnFile
    updateVars()

    
def trlClicked(e):
    cfg["trlangFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.ods"),("all files","*.*")))
    #trlName = os.path.basename(cfg["trlangFile"])
    #trl.delete(0, END)
    #trl.insert(0, trlName)
    updateVars() 
'''
window_size = StringVar()
def winSize(e):
    w = str(center.winfo_width())
    h = str(top_frame.winfo_height()+center.winfo_height()+btm_frame.winfo_height())
    window_size.set(w+'x'+h)
'''
# https://stackoverflow.com/questions/34276663/tkinter-gui-layout-using-frames-and-grid
# create all of the main containers
top_frame = Frame(root, bg='cyan', width=660, height=50, pady=1)
center = Frame(root, bg='gray2', width=650, height=200, padx=1, pady=1)
#center.bind("<Configure>", winSize)
btm_frame = Frame(root, bg='white', width=660, height=45, pady=3)


# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
btm_frame.grid(row=3, sticky="ew")

# create the widgets for the top frame
model_label = Label(top_frame, text='Back Font Utility          -- CSV column order (Glyph, English, Language, Unicode)')

# layout the widgets in the top frame
#model_label.grid(row=0, columnspan=3)
model_label.pack(side = LEFT)

# create the center frames
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = Frame(center, bg='lightblue',   width=200, height=140, padx=3, pady=5)
ctr_right = Frame(center, bg='lightyellow',  width=450, height=210, padx=1, pady=1)
ctr_btm = Frame(center, bg='lightyellow', width=200, height=70, padx=3, pady=3)

cb_label = Label(ctr_btm, text="Generated Files")
cb_label.grid(row=0, columnspan=2)

ctr_left.grid(row=0, column=0, sticky="ns")
ctr_right.grid(row=0, column=1, rowspan=2, sticky="nsew")
ctr_btm.grid(row=1, column=0, sticky="nsew")

# create the bottom frames
btm_left = Frame(btm_frame, width=100, height=45, pady=3)    #, highlightbackground="black", highlightthickness=1)
btm_center = Frame(btm_frame, width=460, height=45, pady=3)  #, highlightbackground="black", highlightthickness=1)
btm_right = Frame(btm_frame, width=100, height=45, pady=3)   #, highlightbackground="black", highlightthickness=1)
btm_left.grid(row=0, column=0, sticky=EW)
btm_center.grid(row=0, column=1, sticky=EW)
btm_right.grid(row=0, column=2, sticky=EW)
btm_frame.grid_rowconfigure(1, weight=1)
btm_frame.grid_columnconfigure(0, weight=1)
btm_frame.grid_columnconfigure(1, weight=2)
btm_frame.grid_columnconfigure(2, weight=1)



#  add widgets to center left
row = 1
lbl0 = Label(ctr_left, bg='lightblue', text="Version", width=8, anchor=W)
lbl0.grid(row=row, column=0, sticky=W)
e0 = Entry(ctr_left, width=10, relief=RIDGE, textvariable=bfClass.version)
e0.grid(row=row, column=1, sticky=W)
e0.bind('<KeyRelease>', lambda *args: versionClicked(bfClass.version))

row = 2
lbl1 = Label(ctr_left, bg='lightblue', text="Language", width=8, anchor=W)
lbl1.grid(row=row, column=0, sticky=W)
e1 = Entry(ctr_left, width=10, textvariable=bfClass.language)
e1.grid(row=row, column=1, sticky=W)
e1.bind('<KeyRelease>', lambda *args: langClicked(bfClass.language))

lbl2 = Label(ctr_left, bg='lightblue', text="Alias", anchor=W)
lbl2.grid(row=row, column=2, sticky=W)
e2 = Entry(ctr_left, width=3, textvariable=bfClass.alias)
e2.grid(row=row, column=3, sticky=W)
e2.bind('<KeyRelease>', lambda *args: aliasClicked(bfClass.alias))

row = 3
lbl3a = Label(ctr_left, bg='lightblue', text="Font File")
lbl3a.grid(column=0, row=row, sticky=W, columnspan=2)
ttf = Entry(ctr_left,width=25)
ttf.grid(column=1, row=row, sticky=W, columnspan=4 )
ttf.insert(0, bfClass.ttf)
ttf.bind("<1>", ttfClicked)

row = 4
lbl3 = Label(ctr_left, bg='lightblue', text="SFD File")
lbl3.grid(column=0, row=row, sticky=W, columnspan=2)
sfd = Entry(ctr_left,width=25)
sfd.grid(column=1, row=row, sticky=W, columnspan=4 )
sfd.insert(0, bfClass.sfdFile)
sfd.bind("<1>", sfdClicked)

row = 5
lbl4 = Label(ctr_left, bg='lightblue', text="KMN File")
lbl4.grid(column=0, row=row, sticky=W, columnspan=2)
kmn = Entry(ctr_left,width=25)
kmn.grid(column=1, row=row, sticky=W, columnspan=4 )
kmn.insert(0, bfClass.kmnFile)
kmn.bind("<1>", kmnClicked)

row = 6
lbl6 = Label(ctr_left, bg='lightblue', text="TRLang File")
lbl6.grid(column=0, row=row, sticky=W, columnspan=2)
trl = Entry(ctr_left,width=25)
trl.grid(column=1, row=row, sticky=W, columnspan=4 )
trl.insert(0, bfClass.trlangFile)
trl.bind("<1>", trlClicked)

# ctr_btm widgets
row = 1
disp0 = Label(ctr_btm, bg='lightyellow', text="PW File")
disp0.grid(row=row, column=0, sticky=W)
disp0 = Label(ctr_btm, textvariable=bfClass.pwFile)
disp0.grid(row=row, column=1, sticky=W)
row = 2
disp1 = Label(ctr_btm, bg='lightyellow', text="Lang File")
disp1.grid(row=row, column=0, sticky=W)
disp1 = Label(ctr_btm, textvariable=bfClass.langFile)
disp1.grid(row=row, column=1, sticky=W)
row = 3
disp2 = Label(ctr_btm, bg='lightyellow', text="Back Font")
disp2.grid(row=row, column=0, sticky=W)
disp2 = Label(ctr_btm, textvariable=bfClass.backFont)
disp2.grid(row=row, column=1, sticky=W)
row = 4
disp3 = Label(ctr_btm, bg='lightyellow', text="kmn_csv File")
disp3.grid(row=row, column=0, sticky=W)
disp3 = Label(ctr_btm, textvariable=bfClass.kmncsv)
disp3.grid(row=row, column=1, sticky=W)
row = 5
disp4 = Label(ctr_btm, bg='lightyellow', text="back2doc File")
disp4.grid(row=row, column=0, sticky=W)
disp4 = Label(ctr_btm, textvariable=bfClass.back2doc)
disp4.grid(row=row, column=1, sticky=W)
row = 6
disp5 = Label(ctr_btm, bg='lightyellow', text="Compact File")
disp5.grid(row=row, column=0, sticky=W)
disp5 = Label(ctr_btm, textvariable=bfClass.compactFile)
disp5.grid(row=row, column=1, sticky=W)

# add textbox to center right
# http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

errBox = scrolledtext.ScrolledText(\
    ctr_right,\
    bg='light cyan', fg='red',\
    width=46, height=5,\
    padx=5, pady=5)
errBox.pack(side=TOP, fill=BOTH, expand = YES)

textBox = scrolledtext.ScrolledText(\
    ctr_right,\
    bg='pale turquoise', fg='blue',\
    width=46, height=20,\
    padx=5, pady=5)
textBox.pack(side=BOTTOM, fill=BOTH, expand = YES)


# issue command scripts
def doCmd(scrpt):
    textBox.update_idletasks()
    errBox.update_idletasks()
    textBox.delete(1.0, END)
    errBox.delete(1.0, END)
    with redirect_stdout(TextIO(textBox)):
        with redirect_stderr(TextIO(errBox)):   
            rc = scrpt()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

# populate bottom panel

dall = Button(btm_center,\
    text = "doall",\
    command = lambda: doCmd(doall)) 
cmdBtns['doall'] = dall
dall.pack(side=LEFT)

bkfnt = Button(btm_center,\
    text = "sfd2csv",\
    command = lambda: doCmd(sfd2csv)) 
bkfnt.pack(side=LEFT)
cmdBtns['sfd2csv'] = bkfnt

kmnfnt = Button(btm_center,\
    text = "kmn2csv",\
    command = lambda: doCmd(kmn2csv))
kmnfnt.pack(side=LEFT)
cmdBtns['kmn2csv'] = kmnfnt

bf2svg = Button(btm_center,\
    text = "csv2svg", \
    command = lambda: doCmd(csv2svg))
bf2svg.pack(side=LEFT)
cmdBtns['csv2svg'] = bf2svg

svg2fnt = Button(btm_center,\
    text = "svg2Font", \
    command =  lambda: doCmd(svg2Font))
svg2fnt.pack(side=LEFT)
cmdBtns['svg2Font'] = svg2fnt

bf2doc = Button(btm_center,\
    text = "back2doc", \
    command = lambda: doCmd(back2doc))
bf2doc.pack(side=LEFT)
cmdBtns['back2doc'] = bf2doc

cmpct = Button(btm_center,\
    text = "compact", \
    #cmd /c fontforge -quiet -script imageRef4x16.py pw%ver%.csv compact%ver%_%alias%.csv
    command = lambda: doCmd(bfCompact))
cmpct.pack(side=LEFT)
cmdBtns['compact4x16'] = cmpct



lfltr = Button(btm_right,\
        text="Filter X",
        command = lambda: efltr.delete(0, END)
    )
lfltr.pack(side=LEFT)
efltr = Entry(btm_right,width=25)
efltr.pack(side=LEFT)
efltr.bind('<Leave>', efltrClicked)

ext = Button(btm_right, text = "Exit", width=10) 
ext.pack(side=RIGHT)
ext.bind("<1>", bfExit)

if __name__ == "__main__":
    bfClass.version.set("76")
    bfClass.alias.set("EN")
    bfClass.language.set("English")
    cfg["eFilter"] = ""
    updateVars()
    
    root.mainloop()