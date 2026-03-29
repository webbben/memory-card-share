@echo off

echo == DEPENDENCY INSTALLER - WINDOWS ==
echo This is the dependency installer for windows. If you're not on a windows machine, you done goofed.
echo We'll install Python, pip, pipenv, and git once you're ready.
pause

REM Install Python 3
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python installation not found. Installing Python 3.12.0...
    curl -o python-installer.exe -L "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
    start /wait python-installer.exe
    del python-installer.exe
    echo Python installation successful! IMPORTANT: Make sure you added Python to PATH during install!
) else (
    echo Python 3 already installed. Nice!
)

REM Install Pip
echo Upgrading pip...
python -m pip install --upgrade pip

python -m pipenv --version >nul 2>nul 
if %errorlevel% neq 0 (
  echo Installing pipenv...
  python -m pip install pipenv
) else (
  echo Pipenv already installed. Nice!
)

REM Install Git
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing git...
    curl -o git-installer.exe -L "https://github.com/git-for-windows/git/releases/download/v2.37.0.windows.1/Git-2.37.0-64-bit.exe"
    start /wait git-installer.exe
    del git-installer.exe
    echo Git installation successful!
) else (
    echo Git already installed. Nice!
)

REM Display versions
echo.
echo Versions:
echo.
python --version
python -m pip --version
python -m pipenv --version
git --version

echo.
echo Setup complete! If any of the version checks above have errors or look wrong, then ask Ben for help with resolving it.
echo.
pause
