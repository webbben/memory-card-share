import git
import os
import json
import time

REPO_URL = "https://github.com/webbben/memory-card-share.git"

def getRepo() -> git.Repo:
    'returns the repo ref object'
    repo_path = get_project_root()
    repo = git.Repo(repo_path)
    return repo

def checkForRemoteChanges():
    '''returns list of memory cards/files that have changed in the remote, and have yet to be pulled to local'''
    repo = getRepo()
    repo.remotes.origin.fetch()

    # compare local files to remote
    local_commit = repo.head.commit
    remote_commit = repo.commit("origin/master")
    diff = repo.git.diff(f"{local_commit.hexsha}..{remote_commit.hexsha}", "--name-only").splitlines()
    changed_cards = [item for item in diff if 'memory-cards' in item]
    return changed_cards

def lockMemoryCard(cardName: str) -> bool:
    'puts a lock on a memory card on github. returns true if successful, or false if the card is already locked.'
    # first, confirm that there is no lock on the card (check github)
    path = os.path.join('memory-cards', cardName, 'lock.json')
    already_locked = does_file_exist_remote(path)
    if already_locked:
        return False
    
    # create the lock json
    username = get_github_username()
    lock_data = {
        "lock_holder": username,
        "held_since": int(time.time())
    }
    with open(path, 'w') as json_file:
        json.dump(lock_data, json_file, indent=2)
    
    # push the lock json to github
    push_to_github(f"{username}: Locked {cardName}")
    return True

def unlockMemoryCard(cardName: str) -> bool:
    '''unlocks a memory card. only fails if the card wasn't locked to begin with'''
    path = os.path.join('memory-cards', cardName, 'lock.json')

    try:
        # Attempt to remove the lock.json file
        os.remove(path)
        return True
    except FileNotFoundError:
        # its already unlocked?
        return False
    except:
        return False


def saveMemoryCardChanges(msg: str = ""):
    'Pushes any existing changes to local memory cards to the remote repo'
    if msg == "":
        msg = "Saved data to memory card in slot A"
    user = get_github_username()
    commitMessage = f"{user}: {msg}"
    push_to_github(commitMessage)

def loadMemoryCardData():
    'Pulls memory card data from the remote repository to local. If there is a merge conflict, the remote will be preferred.'
    repo_path = get_project_root()
    repo = git.Repo(repo_path)

    # first, make sure local changes are committed
    if repo.is_dirty(untracked_files=True):
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

def does_file_exist_remote(remote_path: str) -> bool:
    'checks if the given file exists in the remote repo'
    repo = getRepo()
    repo.remotes.origin.fetch()
    remote_commit = repo.commit('origin/master')
    try:
        # Attempt to get the file from the remote commit
        file_in_remote = remote_commit.tree / remote_path
        return True
    except KeyError:
        return False

def push_to_github(commitMessage: str):
    'pushes all changes to github'
    repo = getRepo()
    repo.git.add(all=True)
    repo.index.commit(commitMessage)
    repo.git.push()

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_github_username() -> str:
    'gets the github username of the user associated with the git configuration'
    repo = getRepo()
    username = repo.config_reader().get_value("user", "name")
    if username == "" or username == None:
        return "Player"
    return username