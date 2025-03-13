NetC off
rem Pulizia della directory di destinazione
rem rmdir o:\Install\NetC\ /S /Q
rem Pulizia della copia eseguibile in locale
rmdir c:\NetC_exe\ /S /Q
pyinstaller NetC.spec
cd dist
rem xcopy NetC o:\Install\NetC\ /S /H /I
xcopy NetC c:\NetC_exe\ /S /H /I
cd ..
rmdir dist /S /Q
rmdir build /S /Q
pause
