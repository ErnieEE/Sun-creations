rem execute pygui2.pygui2

:doit

cmd /c fontforge -quiet -script bfGui.py 
rem python BFdoc.py
rem goto doit

:end