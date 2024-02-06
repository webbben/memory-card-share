import git
import os
import json

REPO_URL = "https://github.com/webbben/memory-card-share.git"


def saveMemoryCardChanges(msg: str = ""):
    'Pushes any existing changes to local memory cards to the remote repo'
    if msg == "":
        msg = "Saved data to memory card in slot A"
    repo_path = get_project_root()
    repo = git.Repo(repo_path)
    user = get_github_username(repo)
    commitMessage = f"{user}: {msg}"
    # add, commit and push
    repo.git.add(all=True)
    repo.index.commit(commitMessage)
    repo.git.push()

def loadMemoryCardData():
    'Pulls memory card data from the remote repository to local. If there is a merge conflict, the remote will be preferred.'
    repo_path = get_project_root()
    repo = git.Repo(repo_path)

    # first, make sure local changes are committed
    repo.git.add(all=True)
    repo.index.commit("save local changes before merging")

    # if there's an unsolvable conflict, we will prefer 'theirs' (i.e. the remote's version of the file)
    repo.remotes.origin.pull(strategy_option='theirs')

def getMemoryCardInfo():
    'Gets all the memory cards currently accessible on the machine'
    dir = "memory-cards"
    output = []

    for cardDir in os.listdir(dir):
        cardDirPath = os.path.join(dir, cardDir)
        if not os.path.isdir(cardDirPath):
            continue

        # check if the card is locked
        json_files = [file for file in os.listdir(cardDirPath) if file.endswith('.json')]
        lock_data = None
        if len(json_files) > 0:
            json_path = os.path.join(cardDirPath, json_files[0])
            with open(json_path, 'r') as json_file:
                lock_data = json.load(json_file)
        
        output.append((cardDir, lock_data))
    
    return output

def getModifiedMemoryCards():
    'returns a list of memory cards (and their subdirectories) that have changes'
    repo = git.Repo(get_project_root())
    repo.remotes.origin.fetch()

    # check for changed memory cards among the modified files
    changedFiles = [item.a_path for item in repo.index.diff(None)]
    memoryCards = [file.split('memory-cards')[1] for file in changedFiles if 'memory-cards' in file]

    return memoryCards


def hardReset():
    '''hard resets the local version of the repo with what's on the remote repo.

    this should only be done as a last resort, if some conflict has happened that's unresolvable between
    the remote and local repos.
    '''

# =========================================================
#
# General Utils
#
# =========================================================

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_github_username(repo: git.Repo):
    'gets the github username of the user associated with the git configuration'
    username = repo.config_reader().get_value("user", "name")
    if username == "" or username == None:
        return "Player"
    return username