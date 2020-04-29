
set primary=pw76.csv
set xrefin=synxref751_76.csv
set kmn="kmnSUN7_6.csv"
set outfile=synxref76.csv

pause besure %kmn% is sorted by unicode

cmd /c fontforge -quiet -script xref.py %xrefin%
cmd /c fontforge -quiet -script synonyms.py %kmn%
cmd /c fontforge -script synxref.py %primary% xref.csv syn.csv %outfile%