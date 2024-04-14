import os
import sys
from typing import Any, List

if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
from dataclasses import dataclass
from enum import Enum

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QIntValidator, QRegularExpressionValidator, QValidator

from Configs.ConfigManager import ConfigManager

schema = {
    "ScrollBar Style": {
        "sScrollbarColor": "#A89984",
        "iScrollbarClickedAlpha": 255,
        "iScrollbarEnterAlpha": 200,
        "bScrollbarUseFade": True,
        "iScrollbarThickness": 18,
        "iScrollbarMinSize": 30,
    },
    "Markdown Styles":{
    'iEditorFontSize': 10,
    'iPreviewFontSize' :10,
    'sEditorBackground': '#dddddd',
    'sPreviewBackground': '#dddddd',
      'sKeyWordColor': '#ea6862',
      'sSymbolColor': '#e78a4e',
      'sStringColor':'#d8a657',
      'sFunctionColor':'#a9b665',
      'sBuiltinColor':'#7daea3',
      'sNumericColor': '#d3869b',
      'sCommentColor': '#928374',
      'sTextColor':'#d4be98',
      'sMarkdownColor':'',
      'sBackGroundColor': '#292828',
      'sCodeFont': 'Cascadia Code',
      'sTextFont':'Calilbri',
      'sIndent1': '#64D8A657', #qt wants argb
      'sIndent2': '#64A9B665',
      'sIndent3': '#64D3869B',
      'sIndent4': '#647DAEA3',
    },
    "Testing": {"sTestingVar1": "asdsa"},
    "Hidden": {# just state keeping vars
        "sLastColor": "#000000",
        "lsSavedStylePath": [],  # user made style json files, use abs path
        "lsSavedStyleNames": [],  # name of each imported style
        "sCurrentStyleName":""
    },  
}


class OptType(int, Enum):
    colorType = 0
    fileType = 1
    intType = 2
    boolType = 3
    floatType = 4
    stringType = 5


@dataclass
class Option:
    varName: str
    repName: str
    desc: str
    type: OptType
    validator: QValidator
    additional: Any = (
        None  # this field is used to storage additional data, like selectable vals for a selector field
    )


colorValidator = QRegularExpressionValidator(
    QRegularExpression(r"#[0-9a-f]{6}", QRegularExpression.PatternOption.CaseInsensitiveOption)
)
ubyteValidator = QIntValidator(0, 255)

# special hinting for each option
optionSchema = [
    Option(
        "sScrollbarColor",
        "Color",
        "Primary color of the scrollbars in markdown editor and preview.",
        OptType.colorType,
        colorValidator,
    ),
    Option(
        "iScrollbarClickedAlpha",
        "Clicked Alpha",
        "Alpha of the bar when clicked down.",
        OptType.intType,
        ubyteValidator,
    ),
    Option(
        "iScrollbarEnterAlpha",
        "Entered Alpha",
        "Alpha of the bar when mouse cursor has entered the scroll area.",
        OptType.intType,
        ubyteValidator,
    ),
    Option(
        "bScrollbarUseFade",
        "Enable Fade",
        "If the scrollbar should fade to transparent when cursor leaves the area. Unchecked means scrollbar is always visible.",
        OptType.boolType,
        None,
    ),
    Option(
        "iScrollbarThickness",
        "Thickness",
        "Thickness/width of the scrollbar",
        OptType.intType,
        QIntValidator(5, 30),
    ),
    Option(
        "iScrollbarMinSize",
        "Min Size",
        "Minimal Size/height of the scrollbar.",
        OptType.intType,
        QIntValidator(15, 100),
    ),
]


class Config(ConfigManager):

    sScrollbarColor : str
    iScrollbarClickedAlpha : int
    iScrollbarEnterAlpha : int
    bScrollbarUseFade : bool
    iScrollbarThickness : int
    iScrollbarMinSize : int
    iEditorFontSize : int
    iPreviewFontSize : int
    sEditorBackground : str
    sPreviewBackground : str
    sKeyWordColor : str
    sSymbolColor : str
    sStringColor : str
    sFunctionColor : str
    sBuiltinColor : str
    sNumericColor : str
    sCommentColor : str
    sTextColor : str
    sBackGroundColor : str
    sCodeFont : str
    sTextFont : str
    sIndent1 : str
    sIndent2 : str
    sIndent3 : str
    sIndent4 : str
    sTestingVar1 : str
    sLastColor : str
    lsSavedStylePath : List[str]
    lsSavedStyleNames : List[str]
    sCurrentStyleName : str


config: Config = None


def getAppConfig() -> Config:
    global config

    if config is None:
        config = ConfigManager(None, os.path.join(os.path.dirname(__file__), "testConfig.ini"), schema, ",")

    return config



if __name__ == "__main__":
    getAppConfig().makeTypeHintClass("Config")
