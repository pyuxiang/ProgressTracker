@echo off

rem Activates environment for editor
rem e.g. `activate atom .` to open Atom in virtual env

rem cd %~p0\.. : move to project root directory
rem .\venv\Scripts\activate : activate the script
rem set FLASK_APP=src/app.py : set flask app filepath in env
rem %* : executes command in arguments

cd %~p0\.. & ^
.\venv\Scripts\activate & ^
set FLASK_APP=src/app.py & ^
%*
