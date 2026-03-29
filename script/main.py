from script.menu import menu
from script.dolphin_cli import getDolphinPath

if __name__ == "__main__":
    loop = True
    # do initial checks 
    dolphinPath = getDolphinPath(False)

    while loop:
        loop = menu(dolphinPath)
