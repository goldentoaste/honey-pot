
from Configs.appConfig import Option, getAppConfig, intType, boolType, colorType
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton, QSizePolicy, QLineEdit, QCheckBox, QSizePolicy 
from PySide6.QtCore import Qt
from PySide6.QtGui import QPageSize
class OptionHolder(QWidget):
    
    def __init__(self,opt:Option ,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.contentChanged = False
        self.opt = opt
        self.config = getAppConfig()
        
        self.hlayout = QHBoxLayout()
        
        self.resetButton = QToolButton()
        self.resetButton.setText("Reset")
        self.resetButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.resetButton.clicked.connect(self.resetValue)

        self.hlayout.addWidget(self.resetButton)
        
        
        self.setLayout(self.hlayout)
        
        
    def resetValue(self):
        '''
        subclass should overrride this
        '''
        raise NotImplementedError()
    
    def getLabel(self) -> QLabel:
        
        label = QLabel(self.opt.repName)
        label.setToolTip(self.opt.desc)
        return label
    
    
class BoolField(OptionHolder):
    
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)
        
        self.checkBox = QCheckBox()
        self.checkBox.setChecked(self.config[self.opt.varName]) # pray the type matches
        self.hlayout.insertWidget(0, self.checkBox)
        self.checkBox.stateChanged.connect (lambda newState:self.config.setValue(self.opt.varName, newState != Qt.CheckState.Unchecked))
    
    def resetValue(self):
        self.checkBox.setChecked(self.config.getDefault(self.opt.varName))


class ColorField(OptionHolder):
    
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)
        
        self.inputField = QLineEdit(self.config[self.opt.varName])
        self.inputField.setValidator(self.opt.validator)
        self.colorButton = QToolButton()
        self.colorButton.setSizePolicy(QSizePolicy.Policy.Preferred,QSizePolicy.Policy.Preferred)
    
    def showColorPicker(self):
        '''
        show a color picker when the color button is clicked.
        '''
    
    def setColor(self, colorStr:str):
        if not colorStr:
            return
        self.inputField.setText(colorStr)
        self.colorButton.setStyleSheet(
            f'''
            QToolButton {{
                background-color: {colorStr}
            }}
            '''
        )
        self.config[self.opt.varName, colorStr]