echo off
python setup.py py2exe
rmdir /s /q dependencies build
del TDGOmniinterface.py
del setup.py
move dist\* .
move dist\lib
rmdir /s /q dist