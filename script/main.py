import git
import os

REPO_URL = "https://github.com/webbben/memory-card-share.git"

def get_project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_github_username(repo: git.Repo):
    'gets the github username of the user associated with the git configuration'
    username = repo.config_reader().get_value("user", "name")
    if username == "" or username == None:
        return "unknown-user"
    return username

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
    'Pulls memory card data from the remote repository to local. Will overwrite any unsaved local changes.'
    repo_path = get_project_root()
    repo = git.Repo(repo_path)
    repo.remotes.origin.pull()

if __name__ == "__main__":
    saveMemoryCardChanges("testing if pushing works properly")