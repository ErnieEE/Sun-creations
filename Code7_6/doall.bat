rem must change system language locale to utf-8
rem https://www.bing.com/search?q=administrative+language+setting+win+10&form=WNSGPH&qs=AS&cvid=7b4667c3e2804c078bbfa20f11d7eb9f&pq=administrative+language+s&cc=US&setlang=en-US&nclid=5DAC70C3F9718B3FD01438C3459AFE25&ts=1581894742795&wsso=Moderate

SETLOCAL

set sfd="SUN7_6.sfd"
set kmn="SUN7_6.kmn"
set ver=76
set ttffont=times.ttf
set alias=EN


cmd /c fontforge -quiet -script bfConfig.py %sfd% %kmn% %ver% %ttffont% %alias% 


if %1.==. goto doall
if %1.== all goto doall
set docmd=%1
echo docmd set
goto %docmd%

:doall
set docmd=all
goto %docmd%

if %docmd% == all (goto backfont) else (goto %docmd%)
echo "shouldn't be here"
goto end
:all
:backfont
rem sequence of commands to build backfont file
:sfd2csv
cmd /c fontforge -quiet -script sfd2csv.py %sfd% dist/pw%ver%_%alias%.csv
if %docmd%  NEQ all (goto end)

:kmn2csv
cmd /c fontforge -quiet -script kmn2csv.py %kmn% dist/kmn%ver%_%alias%.csv
if %docmd%  NEQ all (goto end)

:csv2svg
cmd /c fontforge -quiet -script csv2svg.py dist/pw%ver%_%alias%.csv %ttffont%
if %docmd%  NEQ all (goto end)
cmd /c fontforge -quiet -script svg2Font.py dist/pw%ver%_%alias%.csv %ttffont% %alias% dist/SUNBF%ver%_%alias%
if %docmd%  NEQ all (goto end)

rem following are for documentation and verification
cmd /c fontforge -quiet -script back2doc.py dist/pw%ver%_%alias%.csv dist/back%ver%_%alias%.txt 
if %docmd%  NEQ all (goto end)

:compact
cmd /c fontforge -quiet -script compact4x16.py dist/pw%ver%_%alias%.csv dist/compact%ver%_%alias%.ods
if %docmd%  NEQ all (goto end)

goto end





goto end
rem zipit.bat
rem start /i /b /wait python -c "import util; util.printhi('someInput')"
rem cmd /c python -c "import util; util.zipdir("", %ver%)
:end


