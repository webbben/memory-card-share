@echo off
pipenv install --ignore-pipfile
cd script
pipenv run python main.py