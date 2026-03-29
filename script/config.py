import json
import os
from pathlib import Path

from colorama import Fore
from script.api_handlers import get_project_root, read_json, write_json
from script.utils import clearScreen, displayTitle, fileExists, isYes, pressAnyKey, printc, readInputNum

key_dolphin_path = "dolphin_path"
key_rom_path = "rom_path"
config_filename = "config.json"

def getConfigFilePath() -> str:
    rootDir = get_project_root()
    return os.path.join(rootDir, config_filename)

def ensureConfigFile():
    path = getConfigFilePath()
    f = Path(path)
    if not f.exists():
        write_json(path, {})

def setCustomDolphinPath(dolphinPath: str):
    config_data = read_json(config_filename)
    if config_data == None:
        config_data = {}
    config_data[key_dolphin_path] = dolphinPath 
    write_json(config_filename, config_data)

def getConfigVal(key: str):
    configFile = Path(config_filename)
    if configFile.exists():
        try:
            with open(configFile) as f:
                config = json.load(f)
                val = config.get(key)
                return val
        except:
            pass
    return None

def getCustomDolphinPath() -> str:
    # first, check if a config file exists, and pull a custom dolphin path from there.
    path = getConfigVal(key_dolphin_path) 
    if path != None:
        return str(path) 
    return "" 
    
def setRomPath(romPath):
    f = Path(romPath)
    if not f.exists():
        printc("path doesn't exist", Fore.RED)

    config_data = read_json(config_filename)
    if config_data == None:
        config_data = {}
    config_data[key_rom_path] = romPath 
    write_json(config_filename, config_data)

def getRomPath() -> str:
    path = getConfigVal(key_rom_path)
    if path != None:
        return str(path)
    return ""

def updateConfig():
    clearScreen()
    printc("loading existing config...", Fore.LIGHTBLACK_EX)
    ensureConfigFile()
    customDolphinPath = getCustomDolphinPath()
    romPath = getRomPath()
    clearScreen()

    displayTitle("Update Config")
    printc("Below are the existing configuration values. Choose a config to change, or enter 'Q' to go back.")

    print("[1] Dolphin Path")
    if customDolphinPath == "":
        printc("(Not set)", Fore.LIGHTBLACK_EX)
    else:
        printc(customDolphinPath, Fore.LIGHTCYAN_EX)
    print("[2] Rom Path")
    if romPath == "":
        printc("(Not set)", Fore.LIGHTBLACK_EX)
    else:
        printc(romPath, Fore.LIGHTCYAN_EX)
    print()
    action = input("Enter Option: ") 
    num = readInputNum(action) 
    if num == -1:
        return
    if num == 1:
        dolphinPath = input("Enter Dolphin Path (empty to cancel): ")
        if dolphinPath == "":
            printc("Aborted.")
            pressAnyKey()
            return
        if not fileExists(dolphinPath):
            printc(f"File not found: {dolphinPath}. Make sure there's no typo.", Fore.YELLOW)
            pressAnyKey()
            return
        printc("New dolphin path: " + dolphinPath)
        ans = input("Save? [Y or N]: ")
        if not isYes(ans):
            printc("Aborted.")
            pressAnyKey()
            return
        setCustomDolphinPath(dolphinPath)
        printc("New path set.")
        pressAnyKey()
        return
    if num == 2:
        romPath = input("Enter Rom Path (empty to cancel): ")
        if romPath == "":
            printc("Aborted.")
            pressAnyKey()
            return
        if not fileExists(romPath):
            printc(f"File not found: {romPath}. Make sure there's no typo.", Fore.YELLOW)
            pressAnyKey()
            return
        printc("New rom path: " + romPath)
        ans = input("Save? [Y or N]: ")
        if not isYes(ans):
            printc("Aborted.")
            pressAnyKey()
            return
        setRomPath(romPath)
        printc("New path set.")
        pressAnyKey()
        return
    printc("Hm... I don't think that is a valid option. Try again?", Fore.YELLOW)
    pressAnyKey()
    return

