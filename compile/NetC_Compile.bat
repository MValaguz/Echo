echo on
rmdir build /S /Q
rmdir dist /S /Q
pyinstaller NetC.spec
rmdir build /S /Q
echo I created a unique file using the NetC.spec file
pause