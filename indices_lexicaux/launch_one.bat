rem @echo off

set DIRIN=C:\Users\etudiant\Downloads\CorpusComparable
set DIROUT=C:\Users\etudiant\Downloads\CorpusComparableTAL
set TALIPATH=C:\tools\talismane-distribution-5.1.1-bin
set TALISMANE=-Xmx1G -Dconfig.file=talismane-fr-5.0.4.conf -jar talismane-core-5.1.1.jar --endModule=posTagger --analyse --sessionId=fr --encoding=UTF8
set JAVA="C:\Program Files\Java\jre1.8.0_191\bin\java.exe"

set TARGET=%1
set TARGET=%TARGET:"=%

echo Processing %DIRIN%\%TARGET%

cd %TALIPATH%
%JAVA% %TALISMANE% --inFile=%DIRIN%\%TARGET% --outFile=%DIROUT%\%TARGET%
