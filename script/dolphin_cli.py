import os
import subprocess
from pathlib import Path

from colorama import Fore

from script.api_handlers import get_project_root, getModifiedMemoryCards, getUserLocks, releaseAllUserLocks, saveMemoryCardChanges
from script.config import getCustomDolphinPath, getRomPath
from script.utils import clearScreen, displayTitle, isYes, pressAnyKey, printc

DOLPHIN_PATH_MAC = "/Applications/Dolphin.app/Contents/MacOS/Dolphin"

def getDolphinPath(silent: bool) -> str:
    # first, check if a config file exists, and pull a custom dolphin path from there.
    dolphinPath = getCustomDolphinPath()
    if dolphinPath != "":
        if not silent:
            printc("Custom dolphin path found in config: " + dolphinPath, Fore.LIGHTBLACK_EX)
        return dolphinPath

    dolphinPath = Path(DOLPHIN_PATH_MAC)
    if dolphinPath.exists():
        if not silent:
            printc("Standard dolphin path found (mac OS)", Fore.LIGHTBLACK_EX)
        return DOLPHIN_PATH_MAC
    
    # attempt some random windows paths. I'm not sure if it installs to a standard path in windows though...
    win_paths = [
        r"C:\Program Files\Dolphin\Dolphin.exe",
        r"C:\Program Files (x86)\Dolphin\Dolphin.exe",
        r"D:\Dolphin-x64\Dolphin.exe",
        r"C:\Dolphin-x64\Dolphin.exe",
    ]
    for p in win_paths:
        dolphinPath = Path(p)
        if dolphinPath.exists():
            if not silent:
                printc("Standard dolphin path found (win OS)", Fore.LIGHTBLACK_EX)
            return p 
    
    # no dolphin paths found... 
    if not silent:
        printc("No dolphin path discoverable. Set the path to Dolphin in the config menu.", Fore.LIGHTYELLOW_EX)
    return ""

def seeDolphinStatus():
    clearScreen()
    displayTitle("Dolphin Emulator - Status")
    dolphinPath = getDolphinPath(False)
    if dolphinPath == "":
        printc("No Dolphin path found.", Fore.YELLOW)
        printc("Note: You can set this in the config, if you know the location of your Dolphin executable. Without this, you cannot auto-launch dolphin from this app.")
        pressAnyKey()
        return
    printc("Dolphin path: " + dolphinPath, Fore.LIGHTBLUE_EX)
    getDolphinVersion(dolphinPath)
    print()
    if getRomPath() == "":
        printc("(Rom path not set. Without this, you cannot auto-launch dolphin from this app. Set this in config.)")
    pressAnyKey()

def getDolphinVersion(dolphinPath: str):
    if dolphinPath == "":
        printc("Dolphin path not found.", Fore.YELLOW)
        return 
    result = subprocess.run(
        [dolphinPath,"--version"],
        capture_output=True,
        text=True
    ) 

    output = result.stdout.strip() or result.stderr.strip()

    if result.returncode != 0:
        printc(f"Error running Dolphin: {output}", Fore.RED)
        return

    printc(f"Dolphin version: {output}")

def runDolphin():
    clearScreen()
    displayTitle("Run Dolphin - Autolaunch!")
    dolphinPath = getDolphinPath(True)
    if dolphinPath == "":
        printc("No Dolphin path found.", Fore.YELLOW)
        printc("Since it seems like your Dolphin config isn't set up here, instead, try opening Dolphin and running the game directly from there.")
        printc("If you need help getting the Dolphin path setup, ask Ben for help ;)")
        pressAnyKey()
        return

    pathToRom = getRomPath() 
    if pathToRom == "":
        printc("No rom found.", Fore.YELLOW)
        printc("If you'd like to launch Dolphin directly from here, you should set the path to the rom file in the config.")
        pressAnyKey()
        return

    userLocks = getUserLocks()
    if len(userLocks) == 0:
        printc("You have not checked out any memory cards yet.", Fore.YELLOW)
        pressAnyKey()
        return
    slotA = userLocks[0]
    
    printc("Launch Dolphin directly from here!")
    printc("Once you are done playing, simply close the Dolphin window. Your progress will be automatically saved, and your memory cards will be unlocked.")
    printc("A quicker way to play, instead of having to jump back and forth between here and Dolphin.", Fore.LIGHTBLACK_EX)
    print()
    printc("Rom to launch: " + pathToRom, Fore.LIGHTGREEN_EX)
    printc("Memory card: " + slotA, Fore.LIGHTGREEN_EX)
    printc("(ensure this memory card is set to slot A in Dolphin!)", Fore.LIGHTBLACK_EX)
    ans = input("Launch game? [Y or N]: ")
    if not isYes(ans):
        printc("Aborting game launch.")
        pressAnyKey()
        return

    clearScreen()
    displayTitle("Run Dolphin - Autolaunch!")
    printc("Rom: " + pathToRom, Fore.LIGHTGREEN_EX)
    printc("Memory card: " + slotA, Fore.LIGHTGREEN_EX)
    print()
    printc("Launching Dolphin...")
    printc("Warning: Do NOT close this terminal while playing!", Fore.LIGHTRED_EX)
    print("Once you are finished playing, close the Dolphin window, return here, and wait for your changes to finish saving.")

    args = [dolphinPath, "--exec", pathToRom, "-b"]

    result = subprocess.run(args, capture_output=True, text=True)

    output = result.stdout.strip() or result.stderr.strip()

    if result.returncode != 0:
        printc(f"Error running Dolphin: {output}", Fore.RED)
    else:
        printc("Dolphin exited successfully.", Fore.LIGHTGREEN_EX)

    if len(getModifiedMemoryCards()) > 0:
        printc("Saving changes...")
        saveMemoryCardChanges()
    else:
        printc("No memory card changes found.")

    printc("Releasing all locks...")
    releaseAllUserLocks() 
    printc("Done!", Fore.GREEN)
    pressAnyKey()

def dolphinAutolaunchEnabled() -> bool:
    dolphinPath = getDolphinPath(True)
    if dolphinPath == "":
        return False 
    romPath = getRomPath()
    if romPath == "":
        return False
    return True
