from colorama import Fore, Style
import os
from datetime import datetime
from api_handlers import getMemoryCardInfo, getModifiedMemoryCards, saveMemoryCardChanges, loadMemoryCardData

def checkoutMemoryCard():
    clearScreen()
    # get up to date locks from github
    printc("Loading data from Github...")
    loadMemoryCardData()

    done = False
    warning = ""
    while not done:
        clearScreen()
        displayTitle("Checkout Memory Card")
        printc("Before playing, you should checkout a memory card to use.")
        printc("Doing so reserves a lock on it, so others can't use it and possibly overwrite or corrupt your game data.")
        printc("You are limited to locking 2 memory cards at a time.\n")

        memoryCardInfo = getMemoryCardInfo()

        if len(memoryCardInfo) == 0:
            print("No memory cards found on Github.")
            print("Either this is a bug, or all the memory cards somehow got deleted.")
            print("Tell Ben if this ever happens...")
            pressAnyKey()
            return
        
        currentTime = datetime.utcnow()
        longLock = False
        i = 0
        for (name, lock_info) in memoryCardInfo:
            i += 1
            if lock_info == None:
                printc(f"[{i}] {name}", Fore.LIGHTGREEN_EX)
            else:
                lock_holder = lock_info["lock_holder"]
                held_since = datetime.utcfromtimestamp(int(lock_info["held_since"]))
                time_diff = currentTime - held_since
                hours, remainder = divmod(time_diff, 3600)
                minutes, _ = divmod(remainder, 60)
                timeStr = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
                printc(f"[{i}] {name} [Locked by {lock_holder} for {timeStr}]", Fore.RED)
                if hours > 2:
                    longLock = True
        
        if longLock:
            printc("\nIf a memory card has been locked for a long time, consider contacting the person holding the lock.\n")
        
        # choose the memory card to lock
        print("Which memory card would you like to checkout?\n")
        printc(warning, Fore.LIGHTYELLOW_EX)
        ans = input("Selection (Q to quit): ")
        line = readInputNum(ans)
        if line > 0 and line <= len(memoryCardInfo):
            # attempt to checkout card (line-1)
            print("TODO: checkout card")
            pressAnyKey()
            return
        warning = f"Hmm, option \"{ans}\" don't seem right. Make sure you're entering the line number."


def existingMemoryCards():
    clearScreen()
    displayTitle("Available Memory Cards")
    printc("Below are the memory cards you already have on your system.")
    printc("Load from Github to get the latest data.\n")

    memoryCardInfo = getMemoryCardInfo()
    currentTime = datetime.utcnow()
    longLock = False

    if len(memoryCardInfo) == 0:
        print("(No memory card data on your system.)\n")
    else:
        for (name, lock_info) in memoryCardInfo:
            if lock_info == None:
                printc(name, Fore.LIGHTGREEN_EX)
            else:
                lock_holder = lock_info["lock_holder"]
                held_since = datetime.utcfromtimestamp(int(lock_info["held_since"]))
                time_diff = currentTime - held_since
                hours, remainder = divmod(time_diff, 3600)
                minutes, _ = divmod(remainder, 60)
                timeStr = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
                printc(f"{name} [Locked by {lock_holder} for {timeStr}]", Fore.RED)
                if hours > 2:
                    longLock = True
    
    if longLock:
        printc("\nIf a memory card has been locked for a long time, try reloading from Github.")
        printc("If it's still locked, then consider contacting the person holding the lock.")

    pressAnyKey()

def reviewChanges():
    clearScreen()
    displayTitle("Unsaved Changes")
    printc("Below are changes you've made to memory cards that haven't been saved to Github yet.")
    printc("Once you save to Github, the locks on these memory cards will automatically be released too.\n")

    unsavedChanges = getModifiedMemoryCards()
    if len(unsavedChanges) == 0:
        print("Everything up to date.\n")
        pressAnyKey()
        return
    for file in unsavedChanges:
        printc(file, Fore.GREEN)
    
    printc("\nWould you like to save these changes?")
    ans = input(f"[{colorStr("Y", Fore.GREEN)} or {colorStr("N", Fore.RED)}]: ")
    if not isYes(ans):
        printc("Changes left unsaved.", Fore.LIGHTYELLOW_EX)
        pressAnyKey()
        return
    
    # attempt to save
    saveMemoryCardChanges()
    printc("Save successful!", Fore.GREEN)
    pressAnyKey()

def displayTitle(subtitle: str = ""):
    mainTitle = "YKK INDUSTRIES - ZA GAMECUBE MANAGER"
    underline = "=" * len(mainTitle)
    printc(mainTitle, Fore.LIGHTBLUE_EX)
    if subtitle != "":
        # center the subtitle, if possible
        padding = ""
        if (len(subtitle) < len(mainTitle)):
            padding = round((len(mainTitle) - len(subtitle)) / 2) * " "
        printc(padding + subtitle, Fore.CYAN)
    print(underline + "\n")

def menu():
    'displays the main menu'
    menu_options = [
        ("See existing memory cards", existingMemoryCards),
        ("Reload memory card data", existingMemoryCards),
        ("Checkout a memory card", checkoutMemoryCard),
        ("Save your changes", reviewChanges)
    ]

    done = False
    warning = ""

    while not done:
        clearScreen()

        # display main menu
        displayTitle()
        optNumber = 0
        for (optionTitle, _) in menu_options:
            optNumber += 1
            print(f"[{optNumber}] {optionTitle}")
        print("[Q] Quit")
        printc(warning, Fore.LIGHTYELLOW_EX)

        # handle user input
        action = input("Option: ")
        warning = ""
        if action.lower() == 'q':
            return False
        line = readInputNum(action)
        if line > 0 and line <= len(menu_options):
            # execute menu function for given line
            menu_options[line - 1][1]()
        else:
            warning = f"Huh, option \"{action}\" doesn't seem to be valid. Try again?"
    
    # display menu again
    return True

# =========================================================
#
# General Utils
#
# =========================================================

def pressAnyKey():
    print("")
    input(Fore.LIGHTMAGENTA_EX + "press any key to continue...")

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def printc(s: str, color: str = Fore.MAGENTA):
    print(color + s, Style.RESET_ALL)

def colorStr(s: str, color: str):
    'wraps the given string in the color formatting'
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