@echo off
setlocal

set "SRC=sample.c"
set "OUT=sample.exe"

:: Try to find Visual Studio via vswhere
set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"

if exist "%VSWHERE%" (
    for /f "usebackq tokens=*" %%i in (`"%VSWHERE%" -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath`) do (
        set "VCVARS=%%i\VC\Auxiliary\Build\vcvars64.bat"
    )
)

if defined VCVARS if exist "%VCVARS%" (
    echo Found Visual Studio. Using cl...
    call "%VCVARS%"
    cl "%SRC%" /Fe"%OUT%"
) else (
    echo Visual Studio not found. Falling back to gcc...
    gcc "%SRC%" -o "%OUT%"
)

echo Executing Program Before Modification...
echo ---------------------
"%OUT%"
echo ---------------------
echo.
echo ---------------------
echo Running auto-doc...
python auto-doc.py
echo ---------------------
echo.
echo Executing Program AFTER Modification...
echo ---------------------
"%OUT%"
echo ---------------------

endlocal
