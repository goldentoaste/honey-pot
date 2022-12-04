import os, sys
if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
from Hotkeys.hotkeyManager import HotkeyManager

config: HotkeyManager = None


schema = {
    "debug":{
        "debugKey": "Ctrl+Alt+K"
    }
}

def getKeyConfig():
    global config
    if not config:
        config = HotkeyManager(None, os.path.join(os.path.dirname(__file__), "hotkeys.ini"), schema, {})
    return config

if __name__ =='__main__':
    c = getKeyConfig()
    c.generateConsts()