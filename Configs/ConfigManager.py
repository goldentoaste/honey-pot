import os
from configparser import ConfigParser, NoOptionError, NoSectionError
from typing import Any, Dict, List, Tuple

from PySide6.QtCore import QObject, Signal

"""
This is the PySide6 version
when an option is changed, emit an signal so other widgets can update in response.
"""

"""
schema = {
    "Section Name": {
        ("sOptionName" , val)
    }
}
"""

"""
TODO STRICTLY TYPE LIST CONTENT LATER!!!

- issues
    + list sep cannot be changed once the config file is made, since its not possible to determine what the old sep was.
"""


class ConfigManager(QObject):

    configChanged = Signal(QObject)
    loaded = False

    def __init__(self, parent: QObject, path: str, schema: Dict[str, Tuple[str, Any]], listSep="@@"):

        super().__init__(parent)

        self.path = path  # place to save the config file
        self.listSep: str = listSep

        self.config = ConfigParser()
        self.config.optionxform = str

        self.vals: Dict[str, Any] = {}  # var name mapped to value
        self.secs: Dict[str, str] = {}  # var name mapped to section name

        ##### initializing
        needToSave = False  # if any changes has occured
        if os.path.isfile(path):
            self.config.read(path)

        # missing vars from the config is added from schema
        for section, valDicts in schema.items():
            for name, val in valDicts.items():
                if not self.config.has_section(section):
                    self.config.add_section(section)
                if not self.config.has_option(section, name):
                    self.config.set(section, name, self.getVarString(name, val))

        # load read values in to dicts
        for section in self.config.sections():
            for option in self.config.options(section):
                self.vals[option] = self.loadVar(section, option)
                self.secs[option] = section

        self.loaded = True
        
        self.save()

    def setMultipleVars(self, updates: Dict[str, Any]):
        """
        used to update multiple variables, without calling save for each var

        input is {varName : val, ... }, each varName must exist
        """
        try:
            for key, val in updates.items():
                self.checkVarType(key, val)
                self.vals[key] = val
                self.config.set(self.secs[key], key, self.getVarString(key, val))
            self.save()
        except KeyError as e:
            raise KeyError(
                f"Trying set a config value that doesnt exist! in setMultipleVars\n {updates}"
            ) from e

    def notifyConfigChanged(self):
        self.configChanged.emit(self)

    def __contains__(self, name: str):
        return name in self.vals

    def __getitem__(self, name: str) -> str | int | float | bool | List[str | int | float | bool]:
        return self.vals[name]

    def __setitem__(self, name, val):
        try:
            if self.vals[name] == val:
                return
            self.checkVarType(name, val)
            self.vals[name] = val
            self.config.set(self.secs[name], name, self.getVarString(name, val))
            self.save()
        except KeyError as e:
            raise KeyError(f"Trying to set a config option name which doesnt exist! {name}") from e

    def __setattr__(self, name: str, value: Any) -> None:
        if not self.loaded:
            return super().__setattr__(name, value)
        try:
            if self.vals[name] == value:
                return
            self.checkVarType(name, value)
            self.vals[name] = value
            self.config.set(self.secs[name], name, self.getVarString(name, value))
            self.save()
        except KeyError as e:
            raise AttributeError(f"Trying to set a config value that doesnt exist! {name}") from e

    def __getattribute__(self, name: str):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            try:
                return self.vals[name]
            except KeyError as e:
                raise AttributeError(f"The config attribute is not found: {name}") from e

    def checkVarType(self, name: str, val):
        t = {"s": str, "i": int, "f": float, "b": bool, "l": list}[name[0]]
        if type(val) is not t:
            raise TypeError(f"Type of {name} doesnt match with value : {val}, {type(val)}")

    def getVarString(self, name: str, val: Any):
        return str(val) if name[0] != "l" else self.listSep.join([str(item) for item in val])

    def save(self):
        if not os.path.isdir(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w", encoding="utf-8") as file:
            self.config.write(file)

    def _isBool(self, val: str):
        return val.lower() in ("true", "1", "yes")

    def _loadBool(self, section, option):
        return self._isBool(self.config.get(section, option))

    def loadVar(self, section: str, option: str):
        selector = option[0]
        funcs = {
            "s": self.config.get,
            "i": self.config.getint,
            "f": self.config.getfloat,
            "b": self._loadBool,
        }

        if selector != "l":
            return funcs[selector](section, option)
        listType = option[1]
        listCastings = {"s": lambda x: x, "i": int, "f": float, "b": self._isBool}
        return [listCastings[listType](item) for item in self.config.get(section, option).split(self.listSep)]

    def makeTypeHintClass(self, className: str):

        typeHintStrs = []

        for name in self.vals.keys():
            selector = name[0]
            if selector != "l":
                typeHintStrs.append(
                    f"{name} : " + {"s": "str", "i": "int", "f": "float", "b": "bool"}[selector]
                )
            else:
                listType = {"s": "str", "i": "int", "f": "float", "b": "bool"}[name[1]]
                typeHintStrs.append(f"{name} : List[{listType}]")

        print("")
        print(f"class {className}({self.__class__.__name__}):\n")
        for item in typeHintStrs:
            print(f"    {item}")


if __name__ == "__main__":

    c = ConfigManager(
        None,
        os.path.join(os.path.dirname(__file__), "testConfig.ini"),
        {"main": {"iabc": 123, "bStuff": True, "liWee": [1, 2, 3]}, "Other": {"fFloat": 123.4}},
        listSep=",",
    )
    print(c.iabc)
    c.iabc = False
