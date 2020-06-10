@echo off

rem Start Flask server

cd %~p0\.. & ^
set FLASK_APP=src/app.py & ^
flask run
