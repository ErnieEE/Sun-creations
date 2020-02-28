rem create SUN kmn file from SUN csv dictionary.
rem i.e   fontforge -script csv2kmn.py tr_722_ES.csv SUN723_ES.kmn
rem will use the sun7_23.kmn file as input and generate the sun7_23.csv document file.

set infile=tr_722_es.csv
set ver=722
set lang=es

rem cmd /c fontforge -quiet -script csv2kmn.py %infile% %ver% sun%ver%_%lang%.kmn
cmd /c fontforge -quiet -script csv2kmn.py %infile% %ver% %lang%
