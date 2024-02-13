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

def refreshMemoryCardData() -> bool:
    'reloads memory card data from github. Note: only does this if there are no unsaved local changes.'
    # we don't want to automatically save unsaved memory card changes here, so give up on refreshing
    if len(getModifiedMemoryCards()) > 0:
        return False
    if len(getLocalUnexpectedChanges()) > 0:
        return False
    loadMemoryCardData()
    return True

def createNewMemoryCard(cardName: str) -> str:
    'creates a new memory card and its required sub-folders'
    # first, clean the input name in case it has bad characters
    cardName = cardName.replace(" ", "-") # replace spaces with dashes
    cardName = ''.join(c for c in cardName if (c.isalnum() or c == "-")) # remove non alphanumeric characters
    # make the new card's folder
    newCardPath = get_memory_card_full_path(cardName)
    os.mkdir(newCardPath)
    # make JPN and ENG
    os.mkdir(os.path.join(newCardPath, "JPN"))
    os.mkdir(os.path.join(newCardPath, "USA"))
    # write meta data
    write_json(os.path.join(newCardPath, "meta.json"), { "creator": get_github_username() })
    return cardName

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
    write_json(path, lock_data)

    # push the lock json to github
    push_to_github(f"{username}: Locked {cardName}")
    return True

def getUserLocks() -> list[str]:
    'returns a list of memory cards the current user has locked'
    output = []
    cardInfo = getMemoryCardInfo()
    username = get_github_username()
    for (cardName, lockInfo, _) in cardInfo:
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
        # update meta data
        meta_data_path = os.path.join(get_memory_card_full_path(cardName), 'meta.json')
        meta_data = read_json(meta_data_path)
        if meta_data == None:
            meta_data = {}
        meta_data["last_used_by"] = get_github_username()
        meta_data["last_used_time"] = time.time()
        write_json(meta_data_path, meta_data)
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
    # todo - add some guardrails to make sure we aren't committing anything we don't want to?
    pull_from_github()

def getMemoryCardInfo():
    'Gets all the memory cards currently accessible on the machine'
    dir = get_memory_cards_dir()
    output = []

    for cardDir in os.listdir(dir):
        cardDirPath = os.path.join(dir, cardDir)
        if not os.path.isdir(cardDirPath):
            continue

        # check if the card is locked
        json_files = [file for file in os.listdir(cardDirPath) if file.endswith('lock.json')]
        lock_data = None
        if len(json_files) > 0:
            json_path = os.path.join(cardDirPath, json_files[0])
            lock_data = read_json(json_path)

        # check for meta data
        json_files = [file for file in os.listdir(cardDirPath) if file.endswith('meta.json')]
        meta_data = None
        if len(json_files) > 0:
            json_path = os.path.join(cardDirPath, json_files[0])
            meta_data = read_json(json_path)
        
        output.append((cardDir, lock_data, meta_data))
    
    return output

def getModifiedMemoryCards():
    'returns a list of memory card files that have changes'
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

def remote_has_changes():
    'checks if there are remote changes by comparing the commit hashes'
    repo = getRepo()
    repo.remotes.origin.fetch()
    remote_branch_commit = repo.remote().refs.master.commit
    local_branch_commit = repo.head.commit
    # if the hashes aren't the same, then there are remote changes (since all local commits are immediately uploaded to github)
    return remote_branch_commit != local_branch_commit

def find_local_changes_in_folder(folderName: str):
    'checks if there are local changes in the given directory, and returns the changed file names.'
    repo = git.Repo(get_project_root())
    repo.remotes.origin.fetch()

    # check for changed files with the given folder name among the modified files
    changedFiles = [item.a_path for item in repo.index.diff(None)] + repo.untracked_files
    return [file for file in changedFiles if folderName in file]

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

def pull_from_github():
    'forcibly pulls from github. if there are uncommitted local changes, those are automatically committed. if there are merge conflicts, remote is preferred.'
    repo = getRepo()

    # first, make sure local changes are committed
    if repo.is_dirty(untracked_files=True):
        repo.git.add(all=True)
        repo.index.commit("save local changes before merging")

    # if there's an unsolvable conflict, we will prefer 'theirs' (i.e. the remote's version of the file)
    repo.remotes.origin.pull(strategy_option='theirs')

def push_to_github(commitMessage: str):
    'pushes all memory card changes to github'
    memory_card_files = getModifiedMemoryCards()
    if len(memory_card_files) == 0:
        return
    
    # pull in remote changes before pushing, or else an error can occur
    if remote_has_changes():
        pull_from_github()
    repo = getRepo()
    for file in memory_card_files:
        repo.git.add(file)
    repo.index.commit(commitMessage)
    repo.git.push()

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

def restart():
    'restarts the program'
    os.execl(sys.executable, sys.executable, *sys.argv)

def write_json(path, data):
    'writes a json to a file at the given path, with the given data'
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def read_json(path):
    'reads a json at the given path and returns its data, if it exists'
    if not os.path.exists(path):
        return None
    with open(path, 'r') as file:
        data = json.load(file)
    return data