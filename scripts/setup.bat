@echo off

rem First time setup of repo

rem cd %~p0\.. : move to project root directory
rem python -m venv venv : creates new virtual env with venv
rem .\venv\Scripts\activate : activate the script
rem pip install -r requirements.txt : installs requirements

echo Setting up virtual environment... & ^
cd %~p0\.. & ^
python -m venv venv & ^
.\venv\Scripts\activate & ^
echo Installing requirements... & ^
pip install -r requirements.txt & ^
pause
