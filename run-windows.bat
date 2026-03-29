@echo off

REM go to the directory this script is running in
cd /d "%~dp0"

REM ensure pipenv is installed
python -m pipenv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pipenv...
    python -m pip install pipenv
)

REM check if we pipenv needs to install new dependencies
python -m pipenv install --ignore-pipfile

REM run the python script entry point
python -m pipenv run python -m script.main
