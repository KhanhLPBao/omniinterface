echo off
python setup.py py2exe
rmdir dependencies
rmdir build
del main.py
del setup.py
move dist\* .
rmdir dist