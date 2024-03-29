from colorama import Fore, Style
import os
from datetime import datetime
import api_handlers as api

def displayMemoryCardReport(lineNumbers = False) -> list:
    'displays a report of the memory cards. can optionally add line numbers.'
    memoryCardInfo = api.getMemoryCardInfo()
    username = api.get_github_username()
    if len(memoryCardInfo) == 0:
        print("No memory cards found.")
        print("Either this is a bug, or all the memory cards somehow got deleted.")
        print("Tell Ben if this ever happens...")
        pressAnyKey()
        return []
    
    currentTime = datetime.utcnow()
    longLock = False
    i = 0
    for (name, lock_info, meta_data) in memoryCardInfo:
        i += 1
        if lock_info == None:
            padding = "  " # padding is for the meta data on the second line
            if lineNumbers:
                padding += "  "
                printc(f"[{i}] {name}", Fore.LIGHTGREEN_EX)
            else:
                printc(name, Fore.LIGHTGREEN_EX)
            # add meta data info, if present
            if meta_data:
                last_user = None
                time_since = None
                if "last_used_by" in meta_data:
                    last_user = meta_data["last_used_by"]
                if "last_used_time" in meta_data:
                    timestamp = meta_data["last_used_time"]
                    time_since = timeSince(timestamp)
                if last_user and time_since:
                    printc(f"{padding}Last use: {last_user}, {time_since} ago", Fore.LIGHTBLUE_EX)
        else:
            lock_holder = lock_info["lock_holder"]
            held_since = int(lock_info["held_since"])
            timeStr = timeSince(held_since)
            color = Fore.RED
            # modify display if its locked by the current user
            if lock_holder == username:
                lock_holder = "you"
                color = Fore.LIGHTGREEN_EX
            if lineNumbers:
                printc(f"[{i}] {name} [Locked by {lock_holder} for {timeStr}]", color)
            else:
                printc(f"{name} [Locked by {lock_holder} for {timeStr}]", color)
            if "h" in timeStr:
                longLock = True
    
    if longLock:
        printc("\nIf a memory card has been locked for a long time, consider contacting the person holding the lock.")
        printc("If you're holding a lock and you're done with it, go to the \"Save your changes\" or \"Discard changes\" menu.")
    return memoryCardInfo

def formatDate(timestamp: float) -> str:
    'formats a given timestamp as a human readable date'
    dt_obj = datetime.fromtimestamp(timestamp)
    formatted_date = dt_obj.strftime('%m/%d/%y')
    return formatted_date

def timeSince(timestamp: float) -> str:
    'calculates the approximate time elapsed since the given timestamp, and gives it in a readable string'
    dt_obj = datetime.fromtimestamp(timestamp)
    current_time = datetime.now()

    time_diff = current_time - dt_obj
    days = time_diff.days
    if days > 0:
        return f"{days}d"
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    if hours >= 5:
        return f"{hours}h"
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"

def checkoutMemoryCard():
    clearScreen()
    # get up to date locks from github
    printc("Loading data from Github...")
    api.refreshMemoryCardData()

    done = False
    warning = ""
    while not done:
        clearScreen()
        displayTitle("Checkout Memory Card")
        printc("Before playing, you should checkout a memory card to use.")
        printc("Doing so reserves a lock on it, so others can't use it and possibly overwrite or corrupt your game data.")
        printc("You are limited to locking 2 memory cards at a time.\n")

        memoryCardInfo = displayMemoryCardReport(True)
        if len(memoryCardInfo) == 0:
            return
        
        # choose the memory card to lock
        print("\nWhich memory card would you like to checkout?")
        printc(warning, Fore.LIGHTYELLOW_EX)
        ans = input("Selection (Q to quit): ")
        if isQuit(ans):
            return
        line = readInputNum(ans)
        if line > 0 and line <= len(memoryCardInfo):
            # attempt to check out this memory card
            cardName = memoryCardInfo[line - 1][0]
            if api.lockMemoryCard(cardName):
                printc(f"\nSuccessfully locked {cardName}!", Fore.GREEN)
                print("You're free to play with this memory card in Dolphin now.")
                print("(Don't forget to save to Github and unlock when you're done)")
            else:
                printc(f"\nFailed to lock {cardName}.")
                print("Is it currently locked?")
            pressAnyKey()
            return
        # if the input wasn't valid, notify the user
        warning = f"Hmm, option \"{ans}\" don't seem right. Make sure you're entering the line number."


def viewMemoryCards():
    'displays a simple report of all the memory cards.'
    clearScreen()
    printc("Loading data from github...")
    api.refreshMemoryCardData()

    clearScreen()
    displayTitle("Memory Cards")
    printc("Below are the existing memory cards.\n")

    count = len(displayMemoryCardReport())
    if count == 0:
        return

    pressAnyKey()

def createMemoryCard():
    'walks user through new memory card creation'
    clearScreen()
    printc("Loading data from github...")
    api.refreshMemoryCardData()

    clearScreen()
    displayTitle("Create New Memory Card")
    printc("This utility helps you create a new memory card.")
    printc("It creates the necessary folders, and you handle linking to it in Dolphin.")
    printc("Below are the existing memory cards.\n")

    memoryCardInfo = displayMemoryCardReport()
    cardNames = set()
    for (name, _) in memoryCardInfo:
        cardNames.add(name)

    print("\nWould you like to create a new memory card?")
    ans = input("[Y or N]: ")
    if isYes(ans):
        printc("\nMemory card creation dialog - Enter \"Q\" to quit at any time\n")
        
        # name of memory card
        print("Enter a name for the new memory card.")
        print("Note: special characters will be stripped, and spaces will be converted to dashes to make names code-friendly.")
        valid = False
        while not valid:
            name = input("Name: ")
            if name == "" or isQuit(name):
                printc("Memory card creation cancelled.")
                pressAnyKey()
                return
            if len(name) > 25:
                printc(f"Name is too long ({len(name)} chars). Name should be 25 chars or less.", Fore.YELLOW)
                continue
            if name in cardNames:
                printc(f"Name \"{name}\" is already taken.", Fore.YELLOW)
                continue
            valid = True
        
        clearScreen()
        print("Chosen name for memory card: " + colorStr(name, Fore.GREEN))
        ans = input("Confirm creation? [Y or N]: ")
        if isYes(ans):
            realName = api.createNewMemoryCard(name)
            printc(f"\nMemory card {realName} created!", Fore.GREEN)
            printc("\nMake sure to configure Dolphin to use the created folder now:")
            print(api.get_memory_card_full_path(realName))
            printc("\n(Note: you will probably need to point to the JPN or other region's subfolder)")
            pressAnyKey()
            return
        printc("Memory card creation cancelled.")
        pressAnyKey()
        return
    printc("Memory card creation cancelled.")
    pressAnyKey()

def displayChangesReport(lineNumbers = False) -> int:
    'shows a report of the files that have changed. can optionally add line numbering.'
    unsavedChanges = api.getModifiedMemoryCards()
    if len(unsavedChanges) == 0:
        print("No local unsaved changes.\n")
        pressAnyKey()
        return 0
    i = 0
    for file in unsavedChanges:
        i += 1
        if lineNumbers:
            printc(f"[{i}] {file}", Fore.GREEN)
        else:
            printc(file, Fore.GREEN)
    return len(unsavedChanges)


def reviewChanges():
    'shows the unsaved changes and lets user choose to save them to github'
    clearScreen()
    displayTitle("Unsaved Changes")
    printc("Below are changes you've made to memory cards that haven't been saved to Github yet.")
    printc("Once you save to Github, the locks on these memory cards will automatically be released too.\n")

    count = displayChangesReport()
    if count == 0:
        return
    
    printc("\nWould you like to save these changes?")
    ans = input(f"[{colorStr('Y', Fore.GREEN)} or {colorStr('N', Fore.RED)}]: ")
    if not isYes(ans):
        printc("Changes left unsaved.", Fore.LIGHTYELLOW_EX)
        pressAnyKey()
        return
    
    # attempt to save
    api.saveMemoryCardChanges()
    printc("Save successful!", Fore.GREEN)
    printc("\nUnlock your memory cards?")
    ans = input("[Y or N]: ")
    if isYes(ans):
        api.releaseAllUserLocks()
        printc("all memory cards unlocked!", Fore.GREEN)
    else:
        printc("memory cards left locked. Don't forget to unlock them before closing this app!", Fore.YELLOW)
    pressAnyKey()

def discardChanges():
    'shows unsaved changes and lets user choose to discard them'
    clearScreen()
    displayTitle("Discard Changes")
    printc("Below are changes you've made to memory cards that haven't been saved to Github yet.")
    printc("If you don't want to keep these changes, you can revert the memory cards back to their previous state.")
    printc("Warning! This will delete your changes!", Fore.RED)

    count = displayChangesReport()
    if count == 0:
        return

    printc("\nWould you like to discard these changes?")
    ans = input(f"[{colorStr('Y', Fore.RED)} or {colorStr('N', Fore.GREEN)}]: ")
    if isYes(ans):
        print(f"Confirm that you want to {colorStr('delete', Fore.RED)} these changes (Yes = delete)")
        ans = input("[Y or N]: ")
        if isYes(ans):
            # todo - delete the unsaved data
            printc("Reversed local unsaved changes!", Fore.GREEN)
        else:
            printc("Nothing changed.")
        pressAnyKey()
        return
    printc("Nothing changed.")
    pressAnyKey()

def resetToRemote():
    'menu option for doing hard reset to origin'
    clearScreen()
    displayTitle("Hard Reset (!)")
    printc("This option is for hard reseting your local repository.", Fore.LIGHTRED_EX)
    print(f"In other words, all local files will be {colorStr('wiped out and replaced', Fore.LIGHTRED_EX)} by whatever is in github right now.\n")
    printc("Valid reasons you might do this:")
    printc("1) You think you've messed up some local files and want to cleanly reset to what's on github.")
    printc("2) You want to undo some unsaved changes to a memory card.")
    printc("3) There's an update to this program's source code, and you'd like to install it.\n")
    printc("WARNING: any unsaved game data that hasn't been uploaded to github will be deleted!\n", Fore.LIGHTRED_EX)

    print("Do you want to hard reset?")
    ans = input("[Y or N]: ")
    if isYes(ans):
        print("Are you sure you want to hard reset your files? Enter Yes again to confirm.")
        ans = input("Confirm [Y or N]:")
        if isYes(ans):
            printc("Hard reseting...")
            api.hard_reset()
            printc("Hard reset complete!")
            print("This application will now restart.")
            pressAnyKey()
            api.restart()
            return
        printc("Hard reset cancelled.")
        pressAnyKey()
    printc("Hard reset cancelled.")
    pressAnyKey()

def displayTitle(subtitle: str = ""):
    mainTitle = "YKK INDUSTRIES - ZA GAMECUBE MANAGER"
    underline = "=" * len(mainTitle)
    printc(mainTitle, Fore.GREEN)
    if subtitle != "":
        # center the subtitle, if possible
        padding = ""
        if (len(subtitle) < len(mainTitle)):
            padding = round((len(mainTitle) - len(subtitle)) / 2) * " "
        printc(padding + subtitle, Fore.CYAN)
    print(underline + "\n")

def handleQuit():
    'handles quitting and leaving the menu'
    # returns True if quitting, False if not
    # make sure there are no unsaved changes
    printc("Verifying data is saved...", Fore.LIGHTBLUE_EX)
    unsaved_changes = api.getModifiedMemoryCards()
    if len(unsaved_changes) > 0:
        clearScreen()
        printc("Warning! There are unsaved changes on a memory card.", Fore.LIGHTRED_EX)
        print("Please handle your unsaved changes before leaving.\n")
        for card in unsaved_changes:
            printc(card, Fore.LIGHTYELLOW_EX)
        print("")
        ans = input("Continue exiting anyway? [Y or N]: ")
        if isYes(ans):
            printc("\nOk, but forreal... make sure you come back soon to handle unsaved changes and release memory card locks.")
            printc("If you don't, eventually your changes may be wiped out and your locks automatically released.")
            pressAnyKey()
            return True
        return False
    
    # release any held locks - we can do this safely since there are no unsaved changes
    printc("Releasing all locks...", Fore.LIGHTBLUE_EX)
    success = api.releaseAllUserLocks()
    if not success:
        clearScreen()
        printc("Warning: a memory card failed to unlock for an unknown reason.", Fore.YELLOW)
        printc("Tell Ben this happened and he can take a look, but no saved data was lost so no worries.")
        pressAnyKey()
    return True

def bannerLogic():
    # check if there are corrupted/unexpectedly changed files
    changed_files = api.getLocalScriptChanges()
    if len(changed_files) > 0:
       return ("Files in your scripts directory seem to have changed.\nIf you aren't coding new features, please do a hard reset.", Fore.YELLOW)
    changed_files = api.getLocalUnexpectedChanges()
    if len(changed_files) > 0:
        return ("There are unexpected changes in your local files.\nTo avoid pushing them to github, please do a hard reset.", Fore.YELLOW)
    
    # load data, or complain if there's unsaved local data
    success = api.refreshMemoryCardData()
    if not success:
        return ("It seems you have unsaved memory card changes from your last session. Please save those, and refrain from closing this app before saving next time :)", Fore.YELLOW)

    # check if user's git config is valid
    git_config_status = api.verifyGitConfig()
    if git_config_status[0] == False:
        return (f"Your git config appears to be missing a value for {git_config_status[1]}.\nRefer to the git setup instructions to correct this.", Fore.YELLOW)
    
    # welcome the user
    username = api.get_github_username()
    return (f"Welcome, {username}", Fore.MAGENTA)

def menu():
    'displays the main menu'
    menu_options = [
        ("View all memory cards", viewMemoryCards, "Memory Card Management"),
        ("Checkout a memory card", checkoutMemoryCard),
        ("Create a new memory card", createMemoryCard), #todo
        ("Save your changes", reviewChanges, "Done Playing?"),
        ("Hard Reset (!)", resetToRemote, "Other")
    ]

    done = False
    warning = ""
    banner = bannerLogic()

    while not done:
        clearScreen()
        lockedCards = api.getUserLocks()
        displayTitle()
        # display info banners, as needed
        if banner:
            printc(banner[0], banner[1])
            print("")
            banner = None
        if len(lockedCards) > 0:
            printc(f"You have {len(lockedCards)} memory card(s) checked out.\n", Fore.LIGHTGREEN_EX)
        
        # display menu options
        optNumber = 0
        for menu_opt in menu_options:
            optionTitle = menu_opt[0]
            # a third value represents a group header
            if len(menu_opt) == 3:
                printc(" *  " + menu_opt[2], Fore.LIGHTBLUE_EX)
            optNumber += 1
            print(f"[{optNumber}] {optionTitle}")
        printc("[Q] Quit", Fore.CYAN)
        printc(warning, Fore.LIGHTYELLOW_EX)

        # handle user input
        action = input("Option: ")
        warning = ""

        # make sure everything is set before quitting
        if isQuit(action):
            if handleQuit():
                return False
            continue

        # execute the entered option
        line = readInputNum(action)
        if line > 0 and line <= len(menu_options):
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

def isQuit(s: str):
    temp = s.lower()
    return temp == "q" or temp == "quit"