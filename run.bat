@echo off

cd /d %~dp0

call env\Scripts\activate.bat

start http://127.0.0.1:5000

python src\main.py
