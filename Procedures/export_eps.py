'''
export_glyph.py

fontforge -script export_eps.py "Sun6_0 Font.sfd" ebcd ebda eps

'''
import fontforge
import sys
'''
from Tkinter import * 
import Tkinter, Tkconstants, tkSimpleDialog
 
Tkinter.Tk().withdraw() # Close the root window
fontfile = tkFileDialog.askopenfilename(title = "Select FontForge file",filetypes = (("sfd files","*.sfd"),("all files","*.*")))

uec1 = tkSimpleDialog.askstring("First Unicode ", "Enter the first Unicode")
uec2 = tkSimpleDialog.askstring("Last Unicode ", "Enter the last Unicode")
hex_str = "0x"+uec1
int1 = int(hex_str, 16)
hex_str = "0x"+uec2
int2 = int(hex_str, 16)
#fontfile = sys.argv[1]
#fontfile = 'SUN5_2 Font.sfd'
#hex_str = "0xebb9"
#hex_int = int(hex_str, 16)
'''
try:
	fontfile = sys.argv[1]
	hex_str = "0x"+sys.argv[2]
	int1 = int(hex_str, 16)
	hex_str = "0x"+sys.argv[3]
	int2 = int(hex_str, 16)
	ext = sys.argv[4]
	font = fontforge.open (fontfile)
except EnvironmentError:
    sys.exit (1)
	

for glyph in font:
	unicode = font[glyph].unicode
	if unicode >= int1 and unicode <= int2:
		name = font[glyph].glyphname
		filename = name + '.' + ext
		font[name].export(filename)
		print hex(unicode), filename

print 'done'


'''
import fontforge
F = fontforge.open("perpetua.ttf")
for name in F:
    filename = name + ".png"
    # print name
    F[name].export(filename)
    # F[name].export(filename, 600)     # set height to 600 pixels
'''