@echo off
cd /d %userprofile%\Desktop

set repoUrl="https://github.com/webbben/memory-card-share.git"
set repoName="ZA GAMECUBE MANAGER"
git clone %repoUrl% %repoName%

cd %repoName%
pipenv install

echo Repository cloned and program setup successfully!
echo You can close this window and go to the newly created folder called ^"ZA GAMECUBE MANAGER^".
echo In there, run the file called ^"run-windows.bat^" to start the program.
echo.
echo Note: If you need to run this script again to re-install from scratch, please delete the generated folder first.
echo Not doing so could cause unexpected errors.
pause
