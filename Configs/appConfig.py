
import sys, os
from typing import Literal, Any
if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
from Configs.ConfigManager import ConfigManager
from dataclasses import dataclass
from PySide6.QtGui import QValidator,QRegularExpressionValidator , QIntValidator
from PySide6.QtCore import QRegularExpression
schema = {
    "Style.Scrollbar":{
        "sScrollbarColor": "#A89984",
        "iScrollbarClickedAlpha": 255,
        "iScrollbarHoverAlpha": 200,
        "bScrollbarUseFade":True,
        "iScrollbarThickness": 18,
        "iScrllbarMinSize" : 30,
    },
    "Hidden":{ # just state keeping vars
        "sLastColor":"#000000"
    }
}

colorType = 0
fileType = 1
intType = 2
boolType = 3
floatType = 4
stringType = 5
@dataclass
class Option:
    varName:str
    repName:str
    desc:str
    type: int
    validator:QValidator
    

colorValidator = QRegularExpressionValidator (QRegularExpression(r"#[0-9a-f]{6}", QRegularExpression.PatternOption.CaseInsensitiveOption))
ubyteValidator = QIntValidator(0, 255)

# special hinting for each option
optionSchema = [
   Option(
        "sScrollbarColor",
        "Color",
        "Primary color of the scrollbars in markdown editor and preview.",
        colorType,
        colorValidator
    ),
    Option(
        'iScrollbarClickedAlpha',
        "Clicked Alpha",
        "Alpha of the bar when clicked down.",
        intType,
        ubyteValidator
    ),
    Option(
        'iScrollbarEnterAlpha',
        "Entered Alpha",
        "Alpha of the bar when mouse cursor has entered the scroll area.",
        intType,
        ubyteValidator
    ),
    
    Option(
        'iScrollbarUseFade',
        "Enable Fade",
        "If the scrollbar should fade to transparent when cursor leaves the area. Unchecked means scrollbar is always visible.",
        boolType,
        None
    ),
    Option(
        'iScrollbarThickness',
        "Thickness",
        "Thickness/width of the scrollbar",
        intType,
        QIntValidator(5, 30)
    ),
    Option(
        'iScrollbarMinSize',
        "Min Size",
        "Minimal Size/height of the scrollbar.",
        intType,
        QIntValidator(15, 100)
    ),
]
class Config(ConfigManager):

    sScrollbarColor : str
    iScrollbarClickedAlpha : int
    iScrollbarEnterAlpha : int
    bScrollbarUseFade : bool
    iScrollbarThickness : int
    iScrllbarMinSize : int
    
config : Config= None

def getAppConfig():
    global config 
    
    if config is None:
        config = ConfigManager(None, os.path.join(os.path.dirname(__file__), "testConfig.ini"), schema, ",")
    
    return config

if __name__ == "__main__":
    getAppConfig().makeTypeHintClass("Config")