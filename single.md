
class Config:
    
    instance = None
    
    
    private def __init__(self):
        self.val = "stuff"
        
        
    def static getConfig():
        if instance is null:
            instance = Config()
        return instance

Config.getConfig()