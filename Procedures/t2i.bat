@echo off
rem requirements for this are imagemagick convert function  http://www.imagemagick.org
rem and potrace  http://potrace.sourceforge.net/potrace.1.html
rem  example:
rem rem https://stackoverflow.com/questions/1132601/how-to-convert-a-jpeg-image-into-svg-format-using-imagemagick
rem


IF %1.==. GOTO No1
goto inp1

:No1
 
 @ECHO OFF

	SET WINDOWTITLE="Backfont creation"
	SET QUESTION="Enter font name"
	SET DETAIL=""
	SET DEFAULTANSWER=""

	REM name the vbs file the same as this batch file except .vbs
	set FILENAME=%~n0
	REM echo the vbs
	   echo MSG = InputBox(%QUESTION% ^& VBCRLF ^& VBCRLF ^& VBCRLF ^& %DETAIL%, %WINDOWTITLE%, %DEFAULTANSWER%) >> "%~dp0\%FILENAME%.vbs"
	   echo CreateObject("Scripting.FileSystemObject").OpenTextFile("%~dp0\answer.txt",2,True).Write MSG >>  "%~dp0\%FILENAME%.vbs"
	cscript  "%~dp0\%FILENAME%.vbs"
	del "%~dp0\%FILENAME%.vbs"

	SET /P answer=<"%~dp0\answer.txt"

	del "%~dp0\answer.txt"

	echo you typed "%answer%"
	set ffstring="%answer%"
	goto doit
   
:inp1

set ffstring=

  :_PARAMS_LOOP

  REM There is a trailing space in the next line; it is there for formatting.
  set ffstring=%ffstring%%1 
  echo %1
  SHIFT

  if not "%1"=="" goto _PARAMS_LOOP

  echo %ffstring%

  set ffstring="%ffstring%"
   
:doit

echo ffstring  %ffstring%
echo on
  convert -background white -fill black -font arial -pointsize 144 label:%ffstring%   label.ppm
  potrace -s --flat --tight --width 1000 --height 270 label.ppm  -o "%ffstring%.svg"

echo off
  rem inkscape --file=bf.svg  --without-gui --query-height
  rem inkscape --file=bf1.svg  --without-gui --query-y

 del label.ppm
  
 :end
