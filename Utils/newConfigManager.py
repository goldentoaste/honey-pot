
from configparser import ConfigParser, NoSectionError, NoOptionError

import os
from typing import Dict, List, Any
from PySide6.QtCore import QObject, Signal
'''
This is the PySide6 version
when an option is changed, emit an signal so other widgets can update in response.
'''

'''
schema = {
    "Section Name": {
        "sOptionName": val
    }
}
'''


class ConfigManager(QObject):
    
    configChanged = Signal()
    
    def __init__(self, parent: QObject, path: str, schema: Dict[str, Dict[str, Any]], listSep = "@@"):
        
        super().__init__(parent)
        
        self.path = path # place to save the config file
        self.listSep : str = listSep
        
        self.config = ConfigParser()
        self.config.optionxform = str
        
        self.vals : Dict[str, Any] = {} # var name mapped to value
        self.secs : Dict[str, str] = {} # var name mapped to section name
        
        ##### initializing 
        needToSave = False # if any changes has occured
        if os.path.isfile(path):
            self.config.read(path)
        
        for section in self.config.sections():
            