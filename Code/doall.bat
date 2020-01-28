set sfd="SUN7_24 Font.sfd"
set ver=724
set font=times

goto dist
goto after
rem goto arial
goto times
:arial
rem sequence of commands to build backfont file
rem cmd /c fontforge -quiet -script primarywords.py "SUN7_24 Font.sfd" pw724.csv
rem cmd /c fontforge -quiet -script ffchars.py pw724.csv arial.ttf
rem cmd /c fontforge -quiet -script csv2svg.py sizes.csv english arial.ttf
rem cmd /c fontforge -quiet -script svg2Font.py bf724_arial.sfd sizes.csv arial.ttf  english
rem 
goto end

:times
rem sequence of commands to build backfont file
cmd /c fontforge -quiet -script primarywords.py %sfd% pw%ver%.csv
cmd /c fontforge -quiet -script ffchars.py pw%ver%.csv %font%.ttf
cmd /c fontforge -quiet -script csv2svg.py sizes.csv english %font%.ttf
cmd /c fontforge -quiet -script svg2Font.py %ver% sizes.csv %font%.ttf  english
rem 

goto end

:after
echo 
echo The following files are run after the fonts are loaded into the computer
echo
cmd /c fontforge -script bfwords.py SUNBF%ver%_%font%.sfd bf%ver%%font%.csv"
rem cmd /c fontforge -script bfwords.py bf723_arial.sfd bfarial.csv"
cmd /c fontforge -quiet -script back2doc.py pw%ver%.csv back%ver%.txt 
cmd /c fontforge -quiet -script imageRef4x16.py kmn%ver%.csv %ver%compact.csv

:dist
echo The following files may need to be copied from other directories or converted from csv
copy SUNBF%ver%_%font%.sfd dist
copy SUNBF%ver%_%font%.ttf dist
copy SUN%ver%_from_kmn.ods dist
copy primarywords%ver%.ods dist
copy %ver%compact.ods	   dist
copy back%ver%.odt		   dist
copy SUN%ver%_xref.ods	   dist

rem zipit.bat
rem start /i /b /wait python -c "import util; util.printhi('someInput')"
cmd /c python -c "import util; util.zipdir(dist, %ver%):
:end