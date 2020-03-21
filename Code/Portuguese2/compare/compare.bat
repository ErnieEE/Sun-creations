rem ixpwname = 2
rem ixpwuec = 1 
rem ixkmnname = 1
rem ixkmnuec = 3
set primary=langpw.csv
set secondary=pw76_PT.csv
set out=compare_PT721.csv
fontforge -script compare.py %primary% %secondary% %out%