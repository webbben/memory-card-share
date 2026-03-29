#!/bin/bash

# ensure homebrew is installed
if ! command -v brew &>/dev/null; then
  echo "Installing homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

  # Add brew to PATH (handles Apple Silicon + Intel)
  if [[ -d "/opt/homebrew/bin" ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -d "/usr/local/bin" ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  fi
fi

brew update

# Install Python 3.12.0
if ! command -v python3 &>/dev/null; then
  brew install python

  # Reload PATH immediately
  if [[ -d "/opt/homebrew/bin" ]]; then
    export PATH="/opt/homebrew/bin:$PATH"
  elif [[ -d "/usr/local/bin" ]]; then
    export PATH="/usr/local/bin:$PATH"
  fi
fi

python3 -m pip install --upgrade pip

if ! python3 -m pipenv --version &>/dev/null; then
  echo "installing pipenv..."
  python3 -m pip install --user pipenv
fi

# Install Git
if ! command -v git &>/dev/null; then
  echo "installing git..."
  brew install git

  # Reload PATH immediately
  if [[ -d "/opt/homebrew/bin" ]]; then
    export PATH="/opt/homebrew/bin:$PATH"
  elif [[ -d "/usr/local/bin" ]]; then
    export PATH="/usr/local/bin:$PATH"
  fi
fi

# Confirm installation
echo ""
echo "Final check to ensure everything installed..."
echo "(If any of the following shows an error, then something needs to be resolved.)"
python3 --version
python3 -m pip --version
python3 -m pipenv --version
git --version

