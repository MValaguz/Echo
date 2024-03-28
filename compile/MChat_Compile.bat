echo on
rmdir build /S /Q
rmdir dist /S /Q
pyinstaller MChat.spec
rmdir build /S /Q
echo I created a unique file using the MChat.spec file
pause