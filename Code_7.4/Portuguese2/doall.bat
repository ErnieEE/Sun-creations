rem must change system language locale to utf-8
rem https://www.bing.com/search?q=administrative+language+setting+win+10&form=WNSGPH&qs=AS&cvid=7b4667c3e2804c078bbfa20f11d7eb9f&pq=administrative+language+s&cc=US&setlang=en-US&nclid=5DAC70C3F9718B3FD01438C3459AFE25&ts=1581894742795&wsso=Moderate


set sfd="SUN7_24 Font.sfd"
set ver=76
set font=times
set alias=PT
set language=portuguese


echo add csv2keyman 
echo check level of pn ed11
echo  besure to build kmn dictionary
echo language dictionaries be sure to build keyman file
pause





rem '.' + ' ' > U+E37E
rem '*' + ' ' > U+E390
rem 'pn' + ' ' > U+Ed11
rem 'pos' + ' ' > U+E390

copy ed11*.svg svg
copy e390*.svg svg
copy e37e*.svg svg


rem goto step1
rem goto step2
goto dist

 rem fontforge -quiet -script langprimary.py pw76.csv PT.csv

:step1

copy ed11*.svg svg
copy e390*.svg svg
copy e37e*.svg svg

rem sequence of commands to build backfont file for %language%
rem next line is for initial primary list from sfd 
rem cmd /c fontforge -quiet -script primarywords.py %sfd% pw%ver%.csv
cmd /c fontforge -quiet -script langprimary.py pw%ver%.csv %alias%.csv 
cmd /c fontforge -quiet -script csv2kmn.py %alias%.csv %ver% %alias%
cmd /c fontforge -quiet -script csv2svg.py langpw.csv %language% %font%.ttf
cmd /c fontforge -quiet -script svg2Font.py %ver% langpw.csv %font%.ttf %language%
echo install SUNBF%ver%_%alias%.ttf on the computer
pause
goto end

:step2
echo 
echo The following files are run after the fonts are loaded into the computer
echo
rem cmd /c fontforge -script bfwords.py SUNBF%ver%_PT.sfd bf%ver%_PT.csv"
cmd /c fontforge -quiet -script back2doc.py langpw.csv back%ver%_%alias%.txt 
cmd /c fontforge -quiet -script imageRef4x16.py langpw.csv compact%ver%_%alias%.csv
rem 
goto end


:dist
echo The following files may need to be copied from other directories or converted from
 csv
echo off
echo ("Load, compactxxx.csv into a libreoffice calc spreadsheet")
echo ("Load SUN font.  Resize image columns font size to 32. ")
echo ("Print output should be 4 columns with 16 rows per page.")
echo ("Cell format image column width = .65 text column width = 1.15")
echo ("margins left and right = .5. Set name columns to wrap")
echo ("Export as pdf")
pause
copy SUNBF%ver%_%alias%.sfd dist
copy SUNBF%ver%_%alias%.ttf dist
copy SUN%ver%_%alias%.kmn dist
copy langpw.csv  dist\SUNBF%ver%_%alias%.csv
copy compact%ver%_%alias%.ods	   dist
copy compact%ver%_%alias%.pdf	   dist
copy back%ver%_%alias%.txt		   dist
rem copy readme.odt	dist
rem copy SUN%ver%_xref.ods	   dist

rem zipit.bat
rem start /i /b /wait python -c "import util; util.printhi('someInput')"
rem cmd /c python -c "import util; util.zipdir("", %ver%)
:end
