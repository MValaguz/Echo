Echo off
rem Pulizia della directory di destinazione
rem rmdir o:\Install\Echo\ /S /Q
rem Pulizia della copia eseguibile in locale
rmdir c:\Echo_exe\ /S /Q
pyinstaller Echo.spec
cd dist
rem xcopy Echo o:\Install\Echo\ /S /H /I
xcopy Echo c:\Echo_exe\ /S /H /I
cd ..
rmdir dist /S /Q
rmdir build /S /Q
pause
