echo on
rmdir build /S /Q
rmdir dist /S /Q
pyinstaller Echo.spec
rmdir build /S /Q
echo I created a unique file using the Echo.spec file
pause