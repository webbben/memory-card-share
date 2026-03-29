import json
import os
from pathlib import Path

from colorama import Fore

from script.api_handlers import read_json, write_json
from script.utils import pressAnyKey, printc

DOLPHIN_PATH_MAC = "/Applications/Dolphin.app/Contents/MacOS/Dolphin"
DOLPHIN_PATH_WIN = "C:\\Program Files\\Dolphin\\Dolphin.exe"
config_key_dolphin_path = "dolphin_path"
config_filename = "config.json"

def getDolphinPath(silent: bool) -> str:
    # first, check if a config file exists, and pull a custom dolphin path from there.
    configFile = Path(config_filename)
    if configFile.exists():
        try:
            with open(configFile) as f:
                config = json.load(f)
                path = config.get(config_key_dolphin_path)
                if path and Path(path).exists():
                    if not silent:
                        printc("Custom dolphin path found in config: " + path, Fore.LIGHTBLACK_EX)
                    return path
        except:
            pass

    dolphinPath = Path(DOLPHIN_PATH_MAC)
    if dolphinPath.exists():
        if not silent:
            printc("Standard dolphin path found (mac OS)", Fore.LIGHTBLACK_EX)
        return DOLPHIN_PATH_MAC
    dolphinPath = Path(DOLPHIN_PATH_WIN)
    if dolphinPath.exists():
        if not silent:
            printc("Standard dolphin path found (win OS)", Fore.LIGHTBLACK_EX)
        return DOLPHIN_PATH_WIN

    # no dolphin paths found... 
    if not silent:
        printc("No dolphin path discoverable", Fore.LIGHTYELLOW_EX)
    return ""

def setCustomDolphinPath(dolphinPath: str):
    config_data = read_json(config_filename)
    if config_data == None:
        config_data = {}
    config_data[config_key_dolphin_path] = dolphinPath 
    write_json(config_filename, config_data)

def seeDolphinStatus():
    dolphinPath = getDolphinPath(True)
    if dolphinPath == "":
        printc("No Dolphin path found.", Fore.YELLOW)
        return
    printc("Dolphin path: " + dolphinPath, Fore.LIGHTBLUE_EX)
    pressAnyKey()
    
