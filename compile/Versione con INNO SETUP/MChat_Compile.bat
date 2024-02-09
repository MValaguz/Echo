echo on
rmdir build /S /Q
rmdir dist /S /Q
echo I create a unique file using the MChat.spec file 
pyinstaller MChat.spec
xcopy dist\MChat c:\MChat_exe\ /S /H /I
rmdir dist /S /Q
rmdir build /S /Q
pause