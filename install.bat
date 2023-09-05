echo off
python setup.py py2exe
rmdir /s /p /q dependencies
rmdir /s /p /q build
del main.py
del setup.py
move dist\* .
rmdir /s /p /q dist