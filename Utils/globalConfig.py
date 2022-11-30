from Utils.configManager import ConfigManager
import os

schema = {
    "Scrollbar":{
        "sScrollbarColor": "#A89984",
        "iScrollbarClickedAlpha": 255,
        "iScrollbarEnterAlpha": 190,
        "iScrollbarBGAlpha": 90,
        "bScrollbarUseFade":True,
        "iScrollbarThickness": 20
    }
}

class Config:

    sScrollbarColor : str       
    iScrollbarClickedAlpha : int
    iScrollbarEnterAlpha : int  
    iScrollbarBGAlpha : int     
    bScrollbarUseFade : bool    
    iScrollbarThickness : int   


config : Config= None

def getConfig():
    global config 
    
    if config is None:
        config = ConfigManager(None, os.path.join(os.path.dirname(__file__), "testConfig.ini"), schema, ",")
    
    return config

if __name__ == "__main__":
    getConfig().makeTypeHintClass("Config")