@echo off

set DIRBASE=C:\Users\etudiant\Downloads
set DIRIN=C:\Users\etudiant\Downloads\CorpusComparable
set DIROUT=C:\Users\etudiant\Downloads\CorpusComparableTAL

if not exist %DIROUT% (
    mkdir %DIROUT%
)

forfiles /p %DIRIN% /m *.txt /c "cmd /c %DIRBASE%\launch_one.bat @file"
rem "cmd /c echo @file"
