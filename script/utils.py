import os
from colorama import Fore, Style


def pressAnyKey():
    print("")
    input(Fore.LIGHTMAGENTA_EX + "press any key to continue...")


def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")


def printc(s: str, color: str = Fore.MAGENTA):
    print(color + s, Style.RESET_ALL)


def colorStr(s: str, color: str):
    "wraps the given string in the color formatting"
    return color + s + Style.RESET_ALL


def readInputNum(s: str):
    try:
        parsed_int = int(s)
        return parsed_int
    except:
        return -1


def isYes(s: str):
    temp = s.lower()
    return temp == "y" or temp == "yes"


def isQuit(s: str):
    temp = s.lower()
    return temp == "q" or temp == "quit"

