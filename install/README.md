# Installation Scripts

I put together some scripts to make installation easier. To use a script, I recommend downloading it individually from here and running it. Ideally these are all run with administrator/root privileges so they don't get stopped by permissions.

You can download an individual script by clicking on it to go to its page, and then using the ellipse button on the top right:
![image](https://github.com/webbben/memory-card-share/assets/38891424/f9e173fb-9ccd-4368-ba9b-b9e0daab5ec8)

### Windows

Most of you use Windows, so more effort has gone into streamlining this process :)

1. download the windows/ folder and all its contents. open the folder up in your file explorer.
    - apparently there's no option for downloading an entire folder in github, so you'll need to manually download each file and place them together in the same folder on your computer.
2. run the batch script `setup-wizard.bat` by right clicking and choosing **run as administrator**. This runs through the entire setup process! (you don't need to run the other batch scripts - this one runs them all)
3. Midway through this script, you'll need to get your github personal access token. Follow the instructions for [generating a personal access token](#personal-access-token) and return to the script. You can ignore the other steps that are after generating the personal access token, because this script will handle them for you.
    - once you have the personal access token setup, git will handle authenticating with your github account whenever our program executes git commands
4. If everything appears to have executed correctly... you should be done now!  There should be a folder on your desktop named "ZA GAMECUBE MANAGER". In there, run the batch script called `run-windows.bat`.
   * If you think there were problems or errors during installation or, take a look at the [Common Issues](#common-issues) section at the very bottom of this readme. There I'll be documenting problems that other windows users have had during installation, and possible solutions.

### Mac

1. run the bash script `install-python-mac.sh` to install the dependencies
2. Return to the main instructions and finish the rest of the setup (starting from the [git and github setup](https://github.com/webbben/memory-card-share?tab=readme-ov-file#setting-up-git-and-your-github-account) steps)

### Debian/Ubuntu

1. run the bash script `install-python-debian.sh` to install the dependencies
2. Return to the main instructions and finish the rest of the setup (starting from the [git and github setup](https://github.com/webbben/memory-card-share?tab=readme-ov-file#setting-up-git-and-your-github-account) steps)

# Manual Setup Guide
If you're here, that means you're in one of the below camps:
* Windows: the windows setup wizard didn't work, or had some kind of problem along the way
* Other: you ran the dependencies installer, and now are finishing the rest of the steps
  * Or, perhaps the dependency installer didn't work either!

Either way, the instructions below detail the manual steps you can take to install everything.

These instructions assume that you've never used Python, git, github etc before. If you have, then some (or all) of this may already be taken care of.

I'll split this into the following sections:

-   [How to install this program's dependencies](#installing-the-dependencies)
    -   things like the programming language runtime, for example
    -   Try using the installation script first, before resorting to the manual instructions
-   [How to set up git and your github account](#setting-up-git-and-your-github-account)
    -   so you have the ability to interact with this repository
-   [How to download and run this program](#downloading-this-program)
    -   so you can get playing!
    -   Windows users can just run the default setup script

## Installing the Dependencies

First, let's go over some basic dependencies - we'll walk through setting each of these up, but if you already have Python then some of this may be taken care of already.

These are the dependencies:

-   Python 3 - many operating systems come with this pre-installed
-   pip - Python's package manager. If you have Python you may have this already too.
-   pipenv - a python package that handles making virtual environments for code dependencies. Easy to install using pip.
-   git - version control software that effectively powers this memory card sharing system.

### Installing Python

If you're not sure whether or not you have python installed already, try one of these commands in your terminal:

```shell
python3 --version
```

This should tell you the version of an existing python installation. Instead of `python3` it might also be just `python`.

If this fails and you think you need to install python, try this link:

https://www.python.org/downloads/

Make sure to **restart your terminal session** after installing, so that the $PATH is updated and `python3` commands are recognized.

### Installing Pip and Pipenv

To check if pip and pipenv are installed, you can try the same method as above, i.e.:

```shell
pip --version

pipenv --version
```

If they are not installed, first install **pip**.

#### Pip

For Windows:

1. Download a "get-pip.py" file from the internet with this command:

```shell
curl https://bootst/rap.pypa.io/get-pip.py -o get-pip.py
```

2. Run the downloaded python file, which installs pip for you

```shell
python get-pip.py
```

Pip should be installed now! Confirm its installation by running `pip --version` (You may need to restart the terminal first).
If you run into trouble, try following the instructions here: https://www.geeksforgeeks.org/how-to-install-pip-on-windows/

#### Pipenv

Next, let's install **pipenv**
Pipenv is installed via pip, and is just a tool for encapsulating packages for a python project.

This command should work for all operating systems:

```shell
pip install pipenv
```

### Installing Git

Git is version control software that basically powers this memory card sharing system.
It keeps a central repository for our files and also keeps track of its history.

Windows:
https://git-scm.com/download/win

Mac:

```shell
brew install git
```

Debian/Ubuntu:

```shell
sudo apt-get update
sudo apt-get install git
```

## Setting up git and your Github account

First, create a **github account** at github.com if you don't have one already.
This account is required for you to be able to make edits to this repository (i.e. uploading your memory card data).

Once that's taken care of, let Ben know and send him your user information. He needs to add you to the list of contributors for this repo before we can move forward.

### Git config

We need to set the following config settings for your git installation on your computer now:

-   user.name - your display name
-   user.email - the email you used to make your github account
-   credential.helper - I'll explain this in more detail

Github will require these things so they know who is trying to use this repo.

#### user.name

Let's set up your display name in git. This will be what other users see you as in our little program.

Enter this command, replacing `"Your Name"` with your name (don't forget the quotes):

```shell
git config --global user.name "Your Name"
```

to confirm it worked, you can enter:

```shell
git config user.name
```

#### user.email

Next, enter your email the same way you did for your name:

```shell
git config --global user.email "your-email@domain.com"
```

This needs to be the same email as what you used to make your github account! (I think)

#### credential.helper

This last config setting tells git what to do with your credentials. It basically will tell it to keep your personal access token (next step) saved so you dont need to keep entering it.

```shell
git config --global credential.helper store
```

#### confirm your config

To see all your git config settings, enter:

```shell
git config --list
```

You should see the values you set listed here.

### Personal Access Token

Once you've gotten your user info config for git set, we now need the final piece of identification/authorization for git to work with github: a "personal access token".
This will let git push to this repository, which is required for this program to work.

I've outlined the steps you need to follow below, but this site is what I consulted:

https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

But anyway, follow these steps below:

1. [Generate a personal access token (classic)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)

-   For scopes, make sure to include the "repo" section and all its sub-options
-   For expiration, set it to "No Expiration". This way you don't lose the ability to save and load memory card data from Github in the future.

2. [Use your personal token on the command line](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#using-a-personal-access-token-on-the-command-line)

-   We need to do a test edit so we will be prompted for our credentials. Let's use this repo. The purpose of this step is to enter your personal access token and have it stored by git.
-   Copy the HTTP address for this repo (see image below) and enter `git clone http-address-you-copied`.

![image](https://github.com/webbben/memory-card-share/assets/38891424/c62a1744-82b4-4ad6-ae0d-ba441ab62ff2)

-   in your terminal, navigate to the cloned repo's folder. Once you're in there, enter `git push`. This should prompt you for your credentials.
-   Enter your username, and for the password, paste your **personal access token**. Hit enter, and it should accept the credentials. It'll probably tell you there's nothing to push though, since you've made no edits to any files.

3. _(Optional)_ - test that you are truly allowed to edit this repo

-   If the previous steps succeeded, then you should now be allowed to edit this repo.
-   To test this, you can make a dummy edit to this repo. Please don't edit any important files - you can edit README.md though (or just create a random .txt file)
-   once you've made a change, enter `git add *`, `git commit`, and `git push` to push your change to the repo. You shouldn't be prompted for your username or password this time if everything worked from before.
-   You can also consider undoing your change and pushing that back to the repo, just to keep things clean.

## Downloading this program

This is the moment we've all been waiting for. Hopefully it hasn't been too much trouble getting the aforementioned set up - I kind of forgot how many little things go into using Python, git, github etc.

### Cloning this repository

First, decide on a place in your computer you want to store this program. You'll be going to this location either in a terminal or in your folder browser every time you want to start playing, so choosing your desktop might be a solid choice.

Next, navigate to this folder in your terminal. If you use Windows and decided to use your desktop, for example, you can enter this:

```shell
cd Desktop
```

So, in your terminal, navigate to the location you decided upon (e.g. Desktop) and enter the following command. This command will create a new folder in this location called `memory-card-share`. This is a git repository that is linked to this one here on Github. It contains all the files for this program, including all the memory card data.

```shell
git clone https://github.com/webbben/memory-card-share.git
```

Now you should see the folder for this repository, and inside there should be folders for `/memory-cards`, `/scripts`, and `/install`.
You're ready now! You can either open the folder in a regular file explorer, or keep using the command line.

From here, you can run the program by running the run-<os> file corresponding to your operating system:

Windows: `run-windows.bat`

Unix-like OS: `run-unix.sh`


# Common Issues
Below are some issues that have been encountered by folks while installing.

## Windows

### Python
For whatever reason, it seems that Python installs weirdly on Windows 11. Here are some of the problems:
* the command `python` isn't recognized in the terminal.
  * this implies the system PATH variable doesn't include the path to the python executable.
  * try this: https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/
  * don't forget to reboot your computer and open a new terminal session after fixing
* python is installed in a weird place (the windows store directory?) and/or python opens the windows store when its command is called.
  * I'm not very clear on the details of this, but I believe both Braden and Luke have encountered this. Ask them for more details.
