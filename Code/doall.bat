rem must change system language locale to utf-8
rem https://www.bing.com/search?q=administrative+language+setting+win+10&form=WNSGPH&qs=AS&cvid=7b4667c3e2804c078bbfa20f11d7eb9f&pq=administrative+language+s&cc=US&setlang=en-US&nclid=5DAC70C3F9718B3FD01438C3459AFE25&ts=1581894742795&wsso=Moderate


set sfd="SUN7_24 Font.sfd"
set ver=724
set font=times
set lang=RU



copy ed11*.svg svg
copy e390*.svg svg
copy e37e*.svg svg

rem goto portugese
rem goto portugese_after
rem goto russian
rem goto russian_after
goto dist



:portugese
rem sequence of commands to build backfont file
rem cmd /c fontforge -quiet -script primarywords.py %sfd% pw%ver%.csv
rem cmd /c fontforge -quiet -script ffchars.py pw%ver%.csv %font%.ttf
cmd /c fontforge -quiet -script langprimary.py pw724.csv p.csv langpw.csv
cmd /c fontforge -quiet -script csv2svg.py langpw.csv portugese %font%.ttf
cmd /c fontforge -quiet -script svg2Font.py %ver% langpw.csv %font%.ttf  portugese
goto end

:portugese_after
echo 
echo The following files are run after the fonts are loaded into the computer
echo
rem cmd /c fontforge -script bfwords.py SUNBF%ver%_PT.sfd bf%ver%_PT.csv"
cmd /c fontforge -quiet -script back2doc.py langpw.csv back%ver%_PT.txt 
cmd /c fontforge -quiet -script imageRef4x16.py p.csv compact%ver%_PT.csv
rem 
goto end

:russian
rem sequence of commands to build backfont file
rem cmd /c fontforge -quiet -script primarywords.py %sfd% pw%ver%.csv
cmd /c fontforge -quiet -script langprimary.py pw%ver%.csv langpw.csv
rem config.ini russian = {'index_name': '2','index_unicode': '3','alias': 'RU'}
cmd /c fontforge -quiet -script csv2svg.py langpw.csv russian %font%.ttf
cmd /c fontforge -quiet -script svg2Font.py %ver% langpw.csv %font%.ttf  russian
echo install SUNBF%ver%_%lang%.ttf on the computer
pause
goto end

:russian_after
echo 
echo The following files are run after the fonts are loaded into the computer
echo
rem cmd /c fontforge -script bfwords.py SUNBF%ver%_PT.sfd bf%ver%_PT.csv"
cmd /c fontforge -quiet -script back2doc.py langpw.csv back%ver%_%lang%.txt 
cmd /c fontforge -quiet -script imageRef4x16.py langpw.csv compact%ver%_%lang%.csv
rem 
goto end

:spanish
rem sequence of commands to build backfont file
rem cmd /c fontforge -quiet -script primarywords.py %sfd% pw%ver%.csv
rem cmd /c fontforge -quiet -script ffchars.py pw%ver%.csv %font%.ttf
cmd /c fontforge -quiet -script langprimary.py pw724.csv langpw.csv
rem config.ini spanish = {'char_ascent': '','char_descent': '','index_name': '3','index_unicode': '2','alias': 'ES'}
cmd /c fontforge -quiet -script csv2svg.py langpw.csv spanish %font%.ttf
cmd /c fontforge -quiet -script svg2Font.py %ver% langpw.csv %font%.ttf  spanish
echo install %font%.ttf on the computer
pause
rem goto end
:spanish_after
echo 
echo The following files are run after the fonts are loaded into the computer
echo
rem cmd /c fontforge -script bfwords.py SUNBF%ver%_PT.sfd bf%ver%_PT.csv"
cmd /c fontforge -quiet -script back2doc.py langpw.csv back%ver%_ES.txt 
cmd /c fontforge -quiet -script imageRef4x16.py langpw.csv compact%ver%_ES.csv
rem 
goto end

:dist
echo The following files may need to be copied from other directories or converted from
 csv
echo off
echo for compact_%ver% file
echo ("Load, csv_out.ods into a libreoffice calc spreadsheet")
echo ("Load SUN font.  Resize image columns to 32. ")
echo ("Print output should be 4 columns with 16 rows per page.")
echo ("Cell format image column width = .65 text column width = 1.15")
echo ("margins left and right = .5. Set name columns to wrap")
echo ("Export as pdf")
pause
copy SUNBF%ver%_%lang%.sfd dist
copy SUNBF%ver%_%lang%.ttf dist
rem copy SUN%ver%_from_kmn.ods dist
copy langpw.csv  dist\primarywords%ver%_%lang%.csv
copy compact%ver%_%lang%.ods	   dist
copy back%ver%.odt		   dist
copy SUN%ver%_xref.ods	   dist

rem zipit.bat
rem start /i /b /wait python -c "import util; util.printhi('someInput')"
cmd /c python -c "import util; util.zipdir(dist, %ver%):
:end
echo off
echo for compact_%ver% file
echo ("-------- Done ----------")
echo ("Create a libreoffice richtext document")
echo ("Load, csv_out.ods into a libreoffice calc spreadsheet")
echo ("Load SUN font.  Resize image columns to 32. ")
echo ("Print output should be 4 columns with 16 rows per page.")
echo ("Cell format image column width = .65 text column width = 1.15")
echo ("margins left and right = .5. Set name columns to wrap")
echo ("Export as pdf")