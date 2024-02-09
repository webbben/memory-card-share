@echo off

REM go to the directory this script is running in
cd /d "%~dp0"

REM check if we pipenv needs to install new dependencies
pipenv install --ignore-pipfile

REM run the python script entry point
cd script
pipenv run python main.py
