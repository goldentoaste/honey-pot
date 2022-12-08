
from Configs.appConfig import Option, getAppConfig, intType, boolType, colorType
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton, QSizePolicy


class OptionHolder(QWidget):
    
    def __init__(self,opt:Option ,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.contentChanged = False
        self.opt = opt
        self.config = getAppConfig()
        
        layout = QHBoxLayout()
        
        self.resetButton = QToolButton()
        self.resetButton.setText("Reset")
        self.resetButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        
    def resetValue(self):
        '''
        subclass should overrride this
        '''
        self.
    
    
    def getLabel(self) -> QLabel:
        
        label = QLabel(self.opt.repName)
        label.setToolTip(self.opt.desc)
        return label