#!/bin/bash

# Install Python 3.12.0
if ! command -v python3 &>/dev/null; then
    curl -O https://www.python.org/ftp/python/3.12.0/python-3.12.0-macosx10.9.pkg
    sudo installer -pkg python-3.12.0-macosx10.9.pkg -target /
    rm python-3.12.0-macosx10.9.pkg
fi

# Install Pip and Pipenv
if ! command -v pip &>/dev/null; then
    sudo easy_install pip
fi

if ! command -v pipenv &>/dev/null; then
    pip install --user pipenv
fi

# Install Git
if ! command -v git &>/dev/null; then
    brew install git
fi

# Confirm installation
python3 --version
pip --version
pipenv --version
git --version