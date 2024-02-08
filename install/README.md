# Installation Scripts

I put together some scripts to make installation easier. To use a script, I recommend downloading it individually from here and running it. Ideally these are all run with administrator/root privileges so they don't get stopped by permissions.

You can download an individual script by clicking on it to go to its page, and then using the ellipse button on the top right:
![image](https://github.com/webbben/memory-card-share/assets/38891424/f9e173fb-9ccd-4368-ba9b-b9e0daab5ec8)


### Windows
Most of you use Windows, so more effort has gone into streamlining this process :)

1) run the batch script `install-python-windows.bat` to install the dependencies
2) Return to the main instructions and do the [git and github setup](https://github.com/webbben/memory-card-share?tab=readme-ov-file#setting-up-git-and-your-github-account) steps
    * once you have the personal access token setup, git will handle authenticating with your github account whenever our program executes git commands
3) run the batch script `setup-windows-default.bat`
    * this puts the cloned repo folder on your desktop and sets it up for use

### Mac

1) run the bash script `install-python-mac.sh` to install the dependencies
2) Return to the main instructions and finish the rest of the setup (starting from the [git and github setup](https://github.com/webbben/memory-card-share?tab=readme-ov-file#setting-up-git-and-your-github-account) steps)

### Debian/Ubuntu

1) run the bash script `install-python-debian.sh` to install the dependencies
2) Return to the main instructions and finish the rest of the setup (starting from the [git and github setup](https://github.com/webbben/memory-card-share?tab=readme-ov-file#setting-up-git-and-your-github-account) steps)
