echo on
rmdir build /S /Q
rmdir dist /S /Q
echo I create a unique file using the MChat.spec file 
pyinstaller --windowed --onefile --icon=..\\icons\MChat.ico --clean MChat.spec
rmdir build /S /Q
echo I CREATED THE MCHAT.EXE FILE IN "DIST" DIRECTORY
pause