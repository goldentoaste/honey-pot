import os
import sys

if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
from Hotkeys.hotkeyManager import HotkeyManager, _BaseHotkeyManager

config: HotkeyManager = None

# hoykey names:
#########################
Debugkey = "debugKey"
Wrapstars = "wrapStars"
Italic = "italic"
Bold = "bold"
Strikethrough = "strikeThrough"
Title = "title"
Htmlspace = "htmlSpace"
#########################


schema = {
    "debug": {"debugKey": "Ctrl+Alt+K"},
    "Markdown Editor": {
        "wrapStars": "Ctrl+8",
        "italic": "Ctrl+I",  # behaves the same as wrapStars, does not check for too many stars for now
        "bold": "Ctrl+B",  # wrap stars twice, without like safeguarding behaviours for now,
        "strikeThrough": "Ctrl+`",  # wrap with ~ twice
        "title": "Ctrl+3",  # insert # at beginning of line, ignore selection
        "htmlSpace": "Ctrl+Space",  # insert &nbsp
    },
}


def getKeyConfig(base=False):  # if base, then return a basekeymanager
    global config
    if not config:
        args = (None, os.path.join(os.path.dirname(__file__), "hotkeys.ini"), schema, {})
        if base:
            config = _BaseHotkeyManager(*args)
        else:
            config = HotkeyManager(*args)

    return config


if __name__ == "__main__":
    c = getKeyConfig(True)
    c.generateConsts()
