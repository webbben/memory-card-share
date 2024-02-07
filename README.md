# Memory card share
This repo was made to facilitate sharing virtual gamecube memory cards between friends. It's assumed you're using this with Dolphin emulator on gamecube games.

# Setup Instructions
I'll split this into two sections:
* How to install this program's dependencies
* How to set up git, github, and use this program
* How to set up Dolphin emulator on your computer

## Installing the Dependencies
First, let's go over some basic dependencies - we'll walk through setting each of these up, but if you already have Python then some of this may be taken care of already.

These are the dependencies:
* Python 3 - many operating systems come with this pre-installed
* pip - Python's package manager. If you have Python you may have this already too.
* pipenv - a python package that handles making virtual environments for code dependencies. Easy to install using pip.

**I made some shell scripts to automate installation of all these dependencies!** Go to the /install folder
if you'd like to use those. If you have trouble with them, you can also use the manual instructions provided below.

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

## Setting up your Github account and using this program!

First, create a **github account** at github.com if you don't have one already.
This account is required for you to be able to make edits to this repository (i.e. uploading your memory card data).

Once that's taken care of, let Ben know and send him your user information.  He will add you to the list of contributors.

### Personal Access Token

Next you need to get a personal access token and set it up on your local git installation. This will let git push to this repository, which is required for this program to work.

This website has good instructions:  https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

But below I'll try to outline the steps:
1) Generate a personal access token
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic
- For scopes, make sure to include "repos" (repositories)
2) Use your personal token on the command line
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#using-a-personal-access-token-on-the-command-line
3) Use Git Credential Manager to store the access token
- https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git#git-credential-manager

If you're on windows, you can enter this in the Git Bash terminal. Unix-based systems can use the regular command line.
```shell
git config --global credential.helper manager
```
