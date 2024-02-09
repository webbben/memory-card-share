# Installation Scripts

I put together some scripts to make installation easier. To use a script, I recommend downloading it individually from here and running it. Ideally these are all run with administrator/root privileges so they don't get stopped by permissions.

You can download an individual script by clicking on it to go to its page, and then using the ellipse button on the top right:
![image](https://github.com/webbben/memory-card-share/assets/38891424/f9e173fb-9ccd-4368-ba9b-b9e0daab5ec8)

### Windows

Most of you use Windows, so more effort has gone into streamlining this process :)

1. download the windows/ folder and all its contents. open the folder up in your file explorer.
    - apparently there's no option for downloading an entire folder in github, so you'll need to manually download each file and place them together in the same folder on your computer.
3. run the batch script `setup-wizard.bat` by right clicking and choosing **run as administrator**. This runs through the entire setup process! (you don't need to run the other batch scripts - this one runs them all)
4. Midway through this script, you'll need to get your github personal access token. Follow the instructions for [generating a personal access token](https://github.com/webbben/memory-card-share?tab=readme-ov-file#personal-access-token) and return to the script. You can ignore the other steps in the README after generating the token, since this script will do it for you.
    - once you have the personal access token setup, git will handle authenticating with your github account whenever our program executes git commands

### Mac

1. run the bash script `install-python-mac.sh` to install the dependencies
2. Return to the main instructions and finish the rest of the setup (starting from the [git and github setup](https://github.com/webbben/memory-card-share?tab=readme-ov-file#setting-up-git-and-your-github-account) steps)

### Debian/Ubuntu

1. run the bash script `install-python-debian.sh` to install the dependencies
2. Return to the main instructions and finish the rest of the setup (starting from the [git and github setup](https://github.com/webbben/memory-card-share?tab=readme-ov-file#setting-up-git-and-your-github-account) steps)
