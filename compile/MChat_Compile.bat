echo on
rmdir build /S /Q
rmdir dist /S /Q
echo I create a unique file using the MChat.spec file 
pyinstaller MChat.spec
rmdir build /S /Q
pause