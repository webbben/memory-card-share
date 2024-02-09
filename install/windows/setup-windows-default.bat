@echo off

echo == DEFAULT SETUP - WINDOWS ==
echo This is the default setup installer for windows.
echo In short, we will be cloning the github repo, setting it up for use, and then making sure your git config and authentication are setup correctly.
pause

cd /d %userprofile%\Desktop

echo.
echo Cloning github repository...
set repoUrl="https://github.com/webbben/memory-card-share.git"
set repoName="ZA GAMECUBE MANAGER"
git clone %repoUrl% %repoName%
echo Cloning complete!
echo.

echo Setting up pipenv development environment...
cd %repoName%
pipenv install
echo Pipenv setup complete!
echo.

echo Verifying your git configuration...
git config user.name > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo user.name not set yet.
    set /p USERNAME="Enter your name: "
    git config --global user.name "%USERNAME%"
    echo user.name is now set to: %USERNAME%
    echo.
)
git config user.email > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo user.email not set yet.
    echo Enter the email address you have associated with your github account.
    echo If you forgot, go and check real quick. I'll be patient.
    set /p USEREMAIL="Email address: "
    git config --global user.email "%USEREMAIL%"
    echo user.email is now set to: %USEREMAIL%
    echo.
)
git config credential.helper > nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo credential.helper not set yet.
    git config --global credential.helper store
    echo credential.helper is now set to: store
)
echo.
echo here are your git config settings:
git config user.name
git config user.email
git config credential.helper
echo (if any of these should be changed, refer to the main setup instructions)
echo.
echo git config verification complete!
pause

echo.
echo.
echo == GITHUB CREDENTIALS TEST ==
echo Let's do a test git push to our repository, to make sure you have your git credentials stored correctly.
echo You may be prompted for your github username and password.
echo.
echo for PASSWORD: make sure you enter your personal access token - not your regular password!
echo If you don't know your personal access token yet, please go to the main setup instructions for Git and Github Setup to generate one. Then come back here to continue.
echo (If you've already done this setup, then you shouldn't be prompted for your github credentials.)
pause
echo.
echo.
echo Beginning test push to the github repo...
echo.
echo %DATE% %TIME% > testcommit.txt
git add testcommit.txt
git commit -m "Test commit at %DATE% %TIME%"
git push
echo.
echo Github test push complete!

echo.
echo.
echo == SETUP COMPLETE ==
echo Repository cloned and program setup successfully!
echo You can close this window and go to the newly created folder called ^"ZA GAMECUBE MANAGER^".
echo In there, run the file called ^"run-windows.bat^" to start the program.
echo.
echo Note: If you need to run this script again to re-install from scratch, please delete the generated folder first.
echo Not doing so could cause unexpected errors.
echo.
pause
