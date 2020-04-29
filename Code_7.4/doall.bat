rem must change system language locale to utf-8
rem https://www.bing.com/search?q=administrative+language+setting+win+10&form=WNSGPH&qs=AS&cvid=7b4667c3e2804c078bbfa20f11d7eb9f&pq=administrative+language+s&cc=US&setlang=en-US&nclid=5DAC70C3F9718B3FD01438C3459AFE25&ts=1581894742795&wsso=Moderate


set sfd="SUN7_6.sfd"
set kmn="SUN7_6"
set ver=76
set font=times
set alias=EN
set language=english
echo sort pw and kmn files
echo  besure to build kmn dictionary
echo language dictionaries be sure to build keyman file
pause
rem copy ed11*.svg svg
rem copy e390*.svg svg
rem copy e37e*.svg svg

rem goto backfont
rem goto after
goto dist


:backfont
rem sequence of commands to build backfont file
cmd /c fontforge -quiet -script primarywords.py %sfd% pw%ver%.csv
cmd /c fontforge -quiet -script kmn2csv.py %kmn%.kmn kmn%kmn%.csv
cmd /c fontforge -quiet -script bf2svg.py pw%ver%.csv %language% %font%.ttf
cmd /c fontforge -quiet -script svg2Font.py %ver% pw%ver%.csv %font%.ttf %language%

goto end



:after
echo 
echo The following files are run after the fonts are loaded into the computer
echo
cmd /c fontforge -quiet -script back2doc.py pw%ver%.csv back%ver%.txt 
cmd /c fontforge -quiet -script imageRef4x16.py pw%ver%.csv compact%ver%_%alias%.csv
goto end

:dist
echo build Syn and xref combine them and copy here
pause
echo on
copy SUNBF%ver%_%alias%.sfd 	dist
copy SUNBF%ver%_%alias%.ttf 	dist
copy SUNBF%ver%_%alias%.woff 	dist
copy kmnSUN%ver%_%alias%.csv 	dist
copy pw%ver%.csv				dist\pw%ver%_%alias%.csv
copy compact%ver%_%alias%.pdf	dist
copy back%ver%.txt		  		dist
copy synxref%ver%.csv  			dist
goto end

:xdist
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


rem zipit.bat
rem start /i /b /wait python -c "import util; util.printhi('someInput')"
rem cmd /c python -c "import util; util.zipdir("", %ver%)
:end
