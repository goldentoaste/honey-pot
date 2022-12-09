
from Configs.appConfig import Option, getAppConfig, intType, boolType, colorType
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QToolButton, QSizePolicy, QLineEdit, QCheckBox, QSizePolicy , QColorDialog, QSlider
from PySide6.QtCore import Qt

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
        self.colorButton.clicked.connect(self.showColorPicker)
        self.inputField.setInputMask('\#HHHHHH')
        self.inputField.editingFinished.connect(lambda:self.setColor(self.inputField.text()))

        self.hlayout.insertItem(0, self.colorButton)
        self.hlayout.insertItem(0, self.inputField)
        
        
    def showColorPicker(self):
        '''
        show a color picker when the color button is clicked.
        '''
        c = QColorDialog.getColor(self.config.sLastColor, self.parent())
        
        if c is not None and c.isValid():
            self.setColor(c.name())
    
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
        
        
class IntField(OptionHolder):
    
    
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)
        
        self.inputSlider = QSlider