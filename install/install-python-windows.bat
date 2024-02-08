@echo off

REM Install Python 3
where python3 >nul 2>nul
if %errorlevel% neq 0 (
    echo "Python 3 installation not found. Installing Python 3.12.0..."
    curl -o python-installer.exe -L "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    start /wait python-installer.exe
    del python-installer.exe
    echo "Python installation successful!"
) else (
    echo "Python 3 already installed. Nice!"
)

REM Install Pip
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo "No Pip installation found. Installing..."
    python -m ensurepip --default-pip
    echo "Pip installation successful!"
) else (
    echo "Pip already installed. Nice!"
)

where pipenv >nul 2>nul
if %errorlevel% neq 0 (
    echo "No Pipenv installation found. Installing..."
    pip install pipenv
    echo "Pipenv installation successful!"
) else (
    echo "Pipenv already installed. Nice!"
)

REM Install Git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo "No Git installation found. Installing..."
    curl -o git-installer.exe -L "https://github.com/git-for-windows/git/releases/download/v2.37.0.windows.1/Git-2.37.0-64-bit.exe"
    start /wait git-installer.exe
    del git-installer.exe
    echo "Git installation successful!"
) else (
    echo "Git already installed. Nice!"
)

REM Display versions
echo.
echo "Here are the versions of the dependencies"
echo.
python --version
pip --version
pipenv --version
git --version

echo.
echo "You may close this window now."
echo.
pause