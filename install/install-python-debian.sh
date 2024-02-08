#!/bin/bash

echo "Checking for apt updates..."
sudo apt-get update
echo "apt updates done."
echo
echo

# Install Python 3.12.0 on Debian/Ubuntu
if ! command -v python3 &>/dev/null; then
    echo "Python 3 installation not found. Installing..."
    sudo apt-get install -y python3.12
    echo "Python 3 installation complete!"
else
    echo "Python 3 already installed. Nice!"
fi

# Install Pip and Pipenv
if ! command -v pip &>/dev/null; then
    echo "Pip installation not found. Installing..."
    sudo apt-get install -y python3-pip
    echo "Pip installation complete!"
else
    echo "Pip already installed. Nice!"
fi

if ! command -v pipenv &>/dev/null; then
    echo "Pipenv installation not found. Installing..."
    sudo apt-get install pipenv
    echo "Pipenv installation complete!"
else
    echo "Pipenv already installed. Nice!"
fi

# Install Git
if ! command -v git &>/dev/null; then
    echo "Git installation not found. Installing..."
    sudo apt-get install -y git
    echo "Git installation complete!"
else
    echo "Git already installed. Nice!"
fi

echo
echo
echo "Dependency versions displayed below"
echo
python3 --version
pip --version
pipenv --version
git --version
