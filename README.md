# Memory card share
This repo was made to facilitate sharing virtual gamecube memory cards between friends. It's assumed you're using this with Dolphin emulator on gamecube games.

Below you'll find these main sections:
* [Setup instructions](#setup-instructions) - everything you need to download and configure
* [User Guide](#user-guide) - guide for the basic features and how they are meant to be used

# Setup Instructions
These instructions assume that you've never used Python, git, github etc before. If you have, then some (or all) of this may already be taken care of.

I'll split this into the following sections:
* [How to install this program's dependencies](#installing-the-dependencies)
  * things like the programming language runtime, for example
  * Try using the installation script first, before resorting to the manual instructions
* [How to set up git and your github account](#setting-up-git-and-your-github-account)
  * so you have the ability to interact with this repository
* [How to download and run this program](#downloading-this-program)
  * so you can get playing!
  * Windows users can just run the default setup script

## Installing the Dependencies
First, let's go over some basic dependencies - we'll walk through setting each of these up, but if you already have Python then some of this may be taken care of already.

These are the dependencies:
* Python 3 - many operating systems come with this pre-installed
* pip - Python's package manager. If you have Python you may have this already too.
* pipenv - a python package that handles making virtual environments for code dependencies. Easy to install using pip.
* git - version control software that effectively powers this memory card sharing system.

${{\color{Goldenrod}\Huge{\textsf{  Installation\ Scripts!\ \}}}}\$

I made some scripts that should be able to handle installing these dependencies! Go to the [/install](https://github.com/webbben/memory-card-share/tree/master/install) folder to find out which script you should run.
If you run into problems, you can try the instructions I've outlined below too.


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

Once that's taken care of, let Ben know and send him your user information.  He will add you to the list of contributors.

### Personal Access Token

Next you need to get a personal access token and set it up on your local git installation. This will let git push to this repository, which is required for this program to work.

This website has good instructions:  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

But below I'll try to outline the steps:
1) Generate a personal access token
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic
- For scopes, make sure to include the "repo" section and all its sub-options
- For expiration, set it to "No Expiration". This way you don't lose the ability to save and load memory card data from Github in the future.
2) Use your personal token on the command line
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#using-a-personal-access-token-on-the-command-line
- For this, it will ask you to use `git clone` to attempt to clone a repository. It can be any repository - the point is it will prompt you for credentials, and you can enter the personal access token.
- Once you do this, it's stored in memory for the current terminal session. Without closing the terminal, proceed to the next step
3) Use Git Credential Manager to store the access token
- https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git#git-credential-manager
- After entering the command below in the terminal, the personal access token should now be cached for future use. You should no longer be prompted for a password when cloning or pushing to repos.
- To test this, close your terminal and re-open a new terminal session.  Try cloning the same repo you did before, and confirm that it doesn't make you enter a password.

(for git credential manager)
```shell
git config --global credential.helper manager
```

### Display Name
Let's set up your display name in git.  This will be what other users see you as in our little program.

Enter this command, replacing `"Your Name"` with your name (don't forget the quotes):

(Windows users can once again use the **Git Bash** terminal for these git related commands)
```shell
git config --global user.name "Your Name"
```
to confirm it worked, you can enter:
```shell
git config user.name
```

## Downloading this program
This is the moment we've all been waiting for.  Hopefully it hasn't been too much trouble getting the aforementioned set up - I kind of forgot how many little things go into using Python, git, github etc.

${{\color{Goldenrod}\Huge{\textsf{  Windows\ default\ installation\ script!\ \}}}}\$

If you're using Windows, try using the `setup-windows-default.bat` script found in the [/install folder!](https://github.com/webbben/memory-card-share/tree/master/install) It should handle cloning the repository to a folder on your desktop for easy access, and handle the pipenv setup too.
If everything works, you can then go straight to the folder on your desktop and start it up.

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
You're ready now!  You can either open the folder in a regular file explorer, or keep using the command line.

From here, you can run the program by running the run-<os> file corresponding to your operating system:

Windows: `run-windows.bat`

Unix-like OS: `run-unix.sh`

# User Guide
At this point, it's assumed you've completed the installation and setup completely. The rest of this file will provide guidelines for how this program is intended to be used.

## Running this program!
To start this program, run the "run" file for your OS. This will be `run-windows.bat` or `run-unix.sh`.

This starts up the menu so you can get started!

![image](https://github.com/webbben/memory-card-share/assets/38891424/853eb916-6a70-46b8-90e6-e834db2b3cdc)

Here's a brief description of each menu:
* View all memory cards - shows you the existing memory cards to choose from
* Checkout a memory card - lets you reserve a memory card so you can start playing with it
* Create a new memory card - dialog to walk through creating a new memory card
* Save your changes - run this to save your memory card changes!
* Discard changes - run this to revert your (unsaved) changes back to the version on github
* Quit - quit

TODO - add more details for each option

