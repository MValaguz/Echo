echo off
rem Pulizia della directory di destinazione
rem rmdir o:\Install\MCnet\ /S /Q
rem Pulizia della copia eseguibile in locale
rmdir c:\MCnet_exe\ /S /Q
pyinstaller MCnet.spec
cd dist
rem xcopy MCnet o:\Install\MCnet\ /S /H /I
xcopy MCnet c:\MCnet_exe\ /S /H /I
cd ..
rmdir dist /S /Q
rmdir build /S /Q
pause
