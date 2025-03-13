echo on
rmdir build /S /Q
rmdir dist /S /Q
pyinstaller MCnet.spec
rmdir build /S /Q
echo I created a unique file using the MCnet.spec file
pause