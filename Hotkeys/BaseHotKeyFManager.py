import os
from configparser import ConfigParser
from typing import Dict, List, Tuple

from PySide6.QtCore import QObject, Qt, QThread, Signal
from PySide6.QtGui import QKeySequence, QShortcut


class _BaseHotkeyManager(QObject):

    hotkeysChanged = Signal(QObject)  # emits self when hotkeys configs are changed.

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

    def __init__(
        self, parent: QObject, path: str, schema: Dict[str, Dict[str, str]], globals: List[str]
    ) -> None:
        super().__init__(parent)
        self.schema = schema
        self.path = path
        self.config = ConfigParser()
        self.config.optionxform = str

        if os.path.isfile(path):
            self.config.read(path)
        self.globals = globals
        self.vals: Dict[str, str] = {}  # binding name mapped to key binding str
        self.sections = {}  # binding name mapped to section names

        # add missing values into config
        for section in schema:
            if not self.config.has_section(section):
                self.config.add_section(section)
            for bindingName, binding in schema[section].items():
                if not self.config.has_option(section, bindingName):
                    self.config.set(section, bindingName, binding)

        # load options into memory
        for section in self.config.sections():
            for option in self.config.options(section):
                self.vals[option] = self.config.get(section, option)
                self.sections[option] = section

        self.save()

        self.bindings: Dict[
            QObject, Dict[str, QShortcut]
        ] = {}  # a dict of objects mapped to a dict of their shortcuts
        
    
    def getSection(self):
        return list(self.schema.keys())
    
    def getBindings(self, section:str)-> List[Tuple[str, str]]:
        return [(key,self.vals[key]) for key in self.schema[section].keys()]
    
    def resetBinding(self, name:str)->str:
        '''
        resets the binding the name corresponds to, then return the original keystring
        '''
        originalstr = self.schema[self.sections[name]][name]

        if self.isGlobal(name):
            self.updateGlobalBinding(name, originalstr)
        else:
            self.updateBinding(name, QKeySequence(originalstr))
        return originalstr    
        

    def bindGlobal(self, name: str, signal: Signal):
        raise NotImplementedError()

    def isGlobal(self, name):
        return name in self.globals

    def bindLocal(
        self,
        name: str,
        obj: QObject,
        signal: Signal,
        context: Qt.ShortcutContext = Qt.ShortcutContext.WindowShortcut,
    ):
        """takes the given args, then bind a hotkey sequence to the object.

        Args:
            name (str): name of the hotkey binding
            object (QObject): object to be binded
            signal (Signal): signal to call when binded keys are triggered.
        """
        keySequnce = QKeySequence(self.vals[name], QKeySequence.SequenceFormat.PortableText)
        shortCut = QShortcut(keySequnce, obj, context=context)
        shortCut.activated.connect(signal.emit)
        print("in bind local", name, keySequnce.toString(),keySequnce[0])
        try:
            shortCutDict = self.bindings[obj]
            if name in shortCutDict:
                shortCutDict[name].deleteLater()  # if shortcut of this name already exist, then replace it

            self.bindings[obj][name] = shortCut
        except KeyError:
            self.bindings[obj] = {name: shortCut}

    def updateGlobalBinding(self, name:str, keyStr:str):
        raise NotImplementedError()

    def updateBinding(self, name: str, seq: QKeySequence):
        # DOLATER maybe make this threaded in case it freezes gui

        # updating internal data structures.
        self.vals[name] = seq.toString(QKeySequence.SequenceFormat.PortableText)
        self.config.set(self.sections[name], name, self.vals[name])
        self.save()

        # try updating every registered keybinds that currently exists
        for _, shortcutMap in self.bindings.items():
            for shortcutName, shortcut in shortcutMap.items():
                if shortcutName == name:
                    shortcut.setKey(seq)
                    break  # each name can only occur once

    def clearBindings(self, obj: QObject):
        """
        removes all key bindings for a obj
        """
        for _, shortcut in self.bindings[obj].items():
            shortcut.deleteLater()
        self.bindings.pop(obj)

    def save(self):
        if not os.path.isdir(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w", encoding="utf-8") as file:
            self.config.write(file)

    def generateConsts(self):
        print("\n#hoykey names:\n#########################")
        for val in self.vals:
            print(f"{val.title()} = '{val}'")
        print("#########################\n")
