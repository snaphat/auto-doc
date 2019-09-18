@echo off
gcc sample.c
echo Executing Program Before Modification...
echo ---------------------
a.exe
echo ---------------------
echo.
echo ---------------------
echo Running auto-doc...
python2 auto-doc.py
echo ---------------------
echo.
echo Executing Program AFTER Modification...
echo ---------------------
a.exe
echo ---------------------
