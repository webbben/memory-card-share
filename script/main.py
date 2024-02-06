import git
import os

REPO_URL = "https://github.com/webbben/memory-card-share.git"

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def saveMemoryCardChanges(user: str = "UnknownUser"):
    'Pushes any existing changes to local memory cards to the remote repo'
    repo_path = get_project_root()
    repo = git.Repo(repo_path)
    commitMessage = f"{user}: Saved data to memory card in slot A"
    # add, commit and push
    repo.git.add(all=True)
    repo.index.commit(commitMessage)
    repo.git.push()

def loadMemoryCardData():
    'Pulls memory card data from the remote repository to local. Will overwrite any unsaved local changes.'
    repo_path = get_project_root()
    repo = git.Repo(repo_path)
    repo.remotes.origin.pull()

if __name__ == "__main__":
    saveMemoryCardChanges("webbben")