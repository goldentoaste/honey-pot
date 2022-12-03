
import sys, os

if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
from Configs.ConfigManager import ConfigManager

schema = {
    "Scrollbar":{
        "sScrollbarColor": "#A89984",
        "iScrollbarClickedAlpha": 255,
        "iScrollbarEnterAlpha": 150,
        "iScrollbarHoverAlpha": 200,
        "bScrollbarUseFade":True,
        "iScrollbarThickness": 18,
        "iScrllbarMinSize" : 30,
    }
}
class Config(ConfigManager):

    sScrollbarColor : str
    iScrollbarClickedAlpha : int
    iScrollbarEnterAlpha : int
    iScrollbarHoverAlpha : int
    bScrollbarUseFade : bool
    iScrollbarThickness : int
    iScrllbarMinSize : int
    
config : Config= None

def getConfig():
    global config 
    
    if config is None:
        config = ConfigManager(None, os.path.join(os.path.dirname(__file__), "testConfig.ini"), schema, ",")
    
    return config

if __name__ == "__main__":
    getConfig().makeTypeHintClass("Config")