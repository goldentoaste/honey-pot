import os
from configparser import ConfigParser
from typing import Dict, List

from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtGui import QKeySequence, QShortcut


class _BaseHotkeyManager(QObject):

    hotkeysChnaged = Signal(QObject)  # emits self when hotkeys configs are changed.

    """
    This class should contains all the platform independent stuff, such as 
    help registering widgets with local key bindings, or perhaps showing a gui 
    that lets the user to rebind keys.
    
    Platform depended functions should be a subclass, mostly handling global key bindings,
    which should be using native api calls to register the hotkey for each platform. (just support windows for now)
    """

    """
    hotkey schema
    
    schema = {
        "section name":{
            "binding name": "<key string>" # maybe support more formats later.
        }
    }
    
    should use a config parser to read and write values
    """

    def __init__(self, parent: QObject, path: str, schema: Dict[str, Dict[str, str]]) -> None:
        super().__init__(parent)

        self.path = path
        self.config = ConfigParser()

        if os.path.isfile(path):
            self.config.read(path)

        self.vals = {}  # binding name mapped to key binding str
        self.sections = {}  # binding name mapped to section names

        # add missing values into config
        for section in schema:
            if not self.config.has_section(section):
                self.config.add_section(section)
            for bindingName, binding in schema[section].items():
                if not self.config.has_option(bindingName):
                    self.config.set(section, bindingName, binding)

        # load options into memory
        for section in self.config.sections():
            for option in self.config.options(section):
                self.vals[option] = self.config.get(section, option)
                self.sections[option] = section

        self.save()

    def bindLocal(self, name: str, obj: QObject, signal: Signal):
        """takes the given args, then bind a hotkey sequence to the object.

        Args:
            name (str): name of the hotkey binding
            object (QObject): object to be binded
            signal (Signal): signal to call when binded keys are triggered.
        """
        keySequnce = QKeySequence(self.vals[name], QKeySequence.SequenceFormat.PortableText)
        shortCut = QShortcut(keySequnce, obj)
        obj.__dict__[
            "name"
        ] = shortCut  # giving the reference of the shortcut to the obj itself, so hopefully the hotkey will doestroy itself
        shortCut.activated.connect(signal.emit)

    def save(self):
        if not os.path.isdir(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w", encoding="utf-8") as file:
            self.config.write(file)
