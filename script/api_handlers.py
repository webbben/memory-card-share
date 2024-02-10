import git
import os
import json
import time
import sys

REPO_URL = "https://github.com/webbben/memory-card-share.git"

def getRepo() -> git.Repo:
    'returns the repo ref object'
    repo_path = get_project_root()
    repo = git.Repo(repo_path)
    return repo

def refreshMemoryCardData():
    'reloads memory card data from github. Note: only does this if there are no unsaved local changes.'
    # we don't want to automatically save unsaved memory card changes here, so give up on refreshing
    if len(getModifiedMemoryCards()) > 0:
        return
    loadMemoryCardData()

def createNewMemoryCard(cardName: str) -> bool:
    # make the new card's folder
    newCardPath = get_memory_card_full_path(cardName)
    os.mkdir(newCardPath)
    # make JPN and ENG
    os.mkdir(os.path.join(newCardPath, "JPN"))
    os.mkdir(os.path.join(newCardPath, "USA"))

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
    path = os.path.join(get_memory_card_full_path(cardName), 'lock.json')
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

def getUserLocks() -> list[str]:
    'returns a list of memory cards the current user has locked'
    output = []
    cardInfo = getMemoryCardInfo()
    username = get_github_username()
    for (cardName, lockInfo) in cardInfo:
        if lockInfo:
            if lockInfo["lock_holder"] == username:
                output.append(cardName)
    return output


def releaseAllUserLocks() -> bool:
    '''unlocks all memory cards locked by the current user'''
    lockedMemoryCards = getUserLocks()
    if len(lockedMemoryCards) == 0:
        return True
    
    failures = 0
    for cardName in lockedMemoryCards:
        success = unlockMemoryCard(cardName)
        if not success:
            failures += 1
    
    # push updates to github
    if failures < len(lockedMemoryCards):
        push_to_github(f"{get_github_username()}: All locks released")

    if failures > 0:
        return False
    return True

def unlockMemoryCard(cardName: str) -> bool:
    '''unlocks a memory card. only fails if the card wasn't locked to begin with'''
    path = os.path.join(get_memory_card_full_path(cardName), 'lock.json')

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
    dir = get_memory_cards_dir()
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
    'returns a list of memory cards that have changes'
    changed_files = find_local_changes_in_folder("memory-cards")
    return changed_files

def getLocalScriptChanges():
    'checks if there are local changes to the script directory and returns the changed file names'
    changed_files = find_local_changes_in_folder("script")
    return changed_files

def getLocalUnexpectedChanges():
    'checks if there are any changes in any place outside of the memory-cards directory'
    changed_files = find_local_unexpected_changes()
    return changed_files

def verifyGitConfig():
    'confirm that git config is set as we expect'
    name = get_github_config_value("user", "name")
    if name == None:
        return (False, "user.name")
    email = get_github_config_value("user", "email")
    if email == None:
        return (False, "user.email")
    return (True, "")

# =========================================================
#
# General Utils
#
# =========================================================

def find_local_changes_in_folder(folderName: str):
    'checks if there are local changes in the given directory, and returns the changed file names.'
    repo = git.Repo(get_project_root())
    repo.remotes.origin.fetch()

    # check for changed files with the given folder name among the modified files
    changedFiles = [item.a_path for item in repo.index.diff(None)] + repo.untracked_files
    return [file.split(folderName)[1] for file in changedFiles if folderName in file]

def find_local_unexpected_changes():
    'checks if there are local changes outside of the memory-cards folder in general.'
    repo = git.Repo(get_project_root())
    repo.remotes.origin.fetch()

    # check for changed files with the given folder name among the modified files
    changedFiles = [item.a_path for item in repo.index.diff(None)] + repo.untracked_files
    return [file for file in changedFiles if 'memory-cards' not in file]

def hard_reset():
    '''hard resets the local version of the repo with what's on the remote repo.

    this should only be done as a last resort, if some conflict has happened that's unresolvable between
    the remote and local repos.
    '''
    repo = getRepo()
    repo.remotes.origin.fetch()

    remote_commit = repo.remotes.origin.refs.master.commit
    repo.head.reset(commit=remote_commit, working_tree=True)

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
    'pushes all memory card changes to github'
    repo = getRepo()

    # find modified memory card files
    modified_files = [item.a_path for item in repo.index.diff(None)]
    memory_card_files = [file for file in modified_files if 'memory-cards' in file]
    if len(memory_card_files) == 0:
        return

    for file in memory_card_files:
        repo.git.add(file)
        print(file)
    input("added files")
    repo.index.commit(commitMessage)
    input("committed")
    repo.git.push()
    input("push done")

def get_project_root():
    'gets the absolute path for our project root directory'
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_memory_cards_dir() -> str:
    'gets the absolute path for the memory-cards main storage directory (/memory-cards)'
    rootPath = get_project_root()
    return os.path.join(rootPath, 'memory-cards')

def get_memory_card_full_path(cardName: str) -> str:
    'gets the absolute path for a specific memory card folder (/memory-cards/cardName)'
    rootPath = get_project_root()
    return os.path.join(rootPath, 'memory-cards', cardName)

def get_github_config_value(section: str, option: str):
    'attempts to retrieve a value at the given config setting'
    repo = getRepo()
    # prevent crash if value is unset
    try:
        value = repo.config_reader().get_value(section, option)
    except:
        value = None
    return value

def get_github_username() -> str:
    'gets the github username of the user associated with the git configuration'
    username = get_github_config_value("user", "name")
    if username == None:
        return "Player"
    return username

def exit():
    'exits the program'
    sys.exit()