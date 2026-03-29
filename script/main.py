from script.menu import menu
from script.dolphin_cli import getDolphinPath

if __name__ == "__main__":
    loop = True
    while loop:
        loop = menu()
