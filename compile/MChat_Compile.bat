rmdir o:\Install\MChat\ /S /Q
echo Creo un unico file seguendo le specifiche di MChat.Spec
pyinstaller --windowed --onefile --icon=..\\icons\MChat.ico --clean MChat.spec
cd dist
xcopy  MChat.exe o:\Install\MChat\ /S /H /I
cd ..
rmdir build /S /Q
rmdir dist /S /Q
echo FILE ESEGUIBILE MCHAT.EXE CREATO IN o:\Install\MChat!
pause