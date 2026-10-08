@ECHO OFF
set port=2302
set root=%~dp0
set path=%root%\cg\
set exec=%path%\init.txt

"%root%\haloceded.exe" -path %path% -exec %exec% -port %port%