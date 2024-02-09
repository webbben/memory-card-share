@echo off

echo == WINDOWS SETUP WIZARD ==
echo Welcome to Ben's poorly built setup wizard for windows!
echo.
echo This script will attempt to run other scripts that:
echo 1) install all software dependencies (Python, git, etc)
echo 2) download the github repo to a folder on your Desktop
echo 3) help you setup the required git configuration to authenticate with github
echo.
echo NOTE: if you run this, then you hopefully shouldn't need to run any other installation scripts on your own.
echo.
echo Before running this script, you should go to the README on the github repo's main page, as you might be asked to do some stuff there.
echo If anything crashes or fails, let Ben know. You can also try to walk through the manual steps in the README if all else fails.
echo Alright, let's get started then.
pause

REM call the dependency installer
call install-python-windows.bat

echo.
echo Okay! dependencies should be installed now, assuming everything went smoothly. If the window just opened and then immediately shut, that's a bad sign though lol.
echo Next we are launching the default setup installer. This will handle the last 2 steps. Be prepared to consult the "Git and Github setup" instructions I provided, since you'll be asked for your personal access token.
pause

echo.
echo Alright, at this point everything should be setup correctly.  Try running the run-windows.bat file in the folder that was created on your desktop.
echo If you run into any problems, let Ben know.
echo You can close this window now.
pause