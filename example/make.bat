@echo off
C:\Users\snaph\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.MCF.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin\gcc.exe sample.c -o sample.exe
echo Executing Program Before Modification...
echo ---------------------
sample.exe
echo ---------------------
echo.
echo ---------------------
echo Running auto-doc...
python auto-doc.py
echo ---------------------
echo.
echo Executing Program AFTER Modification...
echo ---------------------
sample.exe
echo ---------------------
