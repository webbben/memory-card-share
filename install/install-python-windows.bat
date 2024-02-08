@echo off

REM Gets the python3 version if it exists
for /f "tokens=2 delims= " %%G in ('python3 --version 2^>nul') do set "pythonVersion=%%G"

REM Check if Python 3 is not installed or its version is below 3.10
if not defined pythonVersion (
    set "installPython=true"
    echo "No python3 installation found."
) else (
    REM Extract major and minor version numbers
    for /f "tokens=1,2 delims=." %%A in ("%pythonVersion%") do (
        set /a majorVersion=%%A
        set /a minorVersion=%%B
    )
    REM If version is below 3.10, upgrade to Python 3.12.0
    if %majorVersion% lss 3 if %minorVersion% lss 10 (
        set "installPython=true"
        echo "Python version %majorVersion%.%minorVersion% found. Lets upgrade to 3.12.0!"
    )
)

REM Install/upgrade Python if needed
if defined installPython (
    echo "Installing Python 3.12.0..."
    curl -o python-installer.exe -L "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    start /wait python-installer.exe
    del python-installer.exe
    echo "Python installation successful!"
)

REM Install Pip
if not exist "%pythonPath%\Scripts\pip.exe" (
    echo "No Pip installation found. Installing..."
    easy_install pip
    echo "Pip installation successful!"
)

REM Install Pipenv
if not exist "%pythonPath%\Scripts\pipenv.exe" (
    echo "No Pipenv installation found. Installing..."
    pip install pipenv
    echo "Pipenv installation successful!"
)

REM Install Git
if not exist "%ProgramFiles%\Git" (
    echo "No Git installation found. Installing..."
    curl -o git-installer.exe -L "https://github.com/git-for-windows/git/releases/download/v2.37.0.windows.1/Git-2.37.0-64-bit.exe"
    start /wait git-installer.exe
    del git-installer.exe
    echo "Git installation successful!"
)

REM Display versions
python --version
pip --version
pipenv --version
git --version

echo.
echo "You may close this window now."
echo.
pause