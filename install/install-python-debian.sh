#!/bin/bash

# Install Python 3.12.0 on Debian/Ubuntu
if ! command -v python3 &>/dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3.12
fi

# Install Pip and Pipenv
if ! command -v pip &>/dev/null; then
    sudo apt-get install -y python3-pip
fi

if ! command -v pipenv &>/dev/null; then
    pip install --user pipenv
fi

# Install Git
if ! command -v git &>/dev/null; then
    sudo apt-get update
    sudo apt-get install -y git
fi

# Confirm installation
python3 --version
pip --version
pipenv --version
git --version