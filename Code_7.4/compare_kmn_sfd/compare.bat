
set primary=pw76.csv
set kmn=kmnSUN7_6.csv
set out=compare.txt
fontforge -script compare.py %primary% %kmn% %out%