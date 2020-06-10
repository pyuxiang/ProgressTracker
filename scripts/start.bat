@echo off

rem Start Flask server

cd %~p0\.. & ^
.\venv\Scripts\activate & ^
set FLASK_APP=src/app.py & ^
set FLASK_ENV=development & ^
flask run
