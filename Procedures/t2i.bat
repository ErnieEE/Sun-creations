@echo off
rem requirements for this are imagemagick convert function  http://www.imagemagick.org
rem and potrace  http://potrace.sourceforge.net/potrace.1.html
rem  example:
rem rem https://stackoverflow.com/questions/1132601/how-to-convert-a-jpeg-image-into-svg-format-using-imagemagick
rem


IF %1.==. GOTO No1
goto inp1

:No1
    rem echo "no1"
   set /p ffstring= "Enter font name "
   set ffstring="%ffstring%"
   echo %ffstring%
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
  potrace -s --flat --tight label.ppm  -o bf.svg
echo off
  rem inkscape --file=bf.svg  --without-gui --query-height
  rem inkscape --file=bf1.svg  --without-gui --query-y

 del label.ppm
  
 :end