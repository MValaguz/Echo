echo off
rem Pulizia della directory di destinazione
rem rmdir o:\Install\MChat\ /S /Q
rem Pulizia della copia eseguibile in locale
rmdir c:\MChat_exe\ /S /Q
pyinstaller MChat.spec
cd dist
rem xcopy MChat o:\Install\MChat\ /S /H /I
xcopy MChat c:\MChat_exe\ /S /H /I
cd ..
rmdir dist /S /Q
rmdir build /S /Q
pause
