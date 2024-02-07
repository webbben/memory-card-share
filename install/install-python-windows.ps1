# Install Python (we're installing specifically 3.12.0)
if (-not (Test-Path "$env:ProgramFiles\Python\Python3.12.0")) {
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.x.x/python-3.12.0-amd64.exe" -OutFile "python-installer.exe"
    Start-Process -Wait -FilePath "python-installer.exe"
    Remove-Item "python-installer.exe"
}

# Add Python and Pip to the PATH so they can be called here
$pythonPath = (Get-Command python).Path
[Environment]::SetEnvironmentVariable("Path", "$env:Path;$pythonPath;$(Split-Path $pythonPath -Parent)", [System.EnvironmentVariableTarget]::Machine)

# Install Pip
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Invoke-Expression "& $pythonPath\Scripts\easy_install.exe pip"
}

# Install Pipenv
if (-not (Get-Command pipenv -ErrorAction SilentlyContinue)) {
    pip install pipenv
}

# Display versions just to confirm
python --version
pip --version
pipenv --version
