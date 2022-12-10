from typing import Dict, List

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (QCheckBox, QColorDialog, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QSizePolicy, QComboBox,
                               QSlider, QToolButton, QVBoxLayout, QWidget)

from Configs.appConfig import Option, OptType, getAppConfig


class OptionHolder(QWidget):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
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
        """
        subclass should overrride this
        """
        raise NotImplementedError()

    def getLabel(self) -> QLabel:

        label = QLabel(self.opt.repName)
        label.setToolTip(self.opt.desc)
        return label


class BoolField(OptionHolder):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)

        self.checkBox = QCheckBox()
        self.checkBox.setChecked(self.config[self.opt.varName])  # pray the type matches
        self.hlayout.insertWidget(0, self.checkBox)
        self.checkBox.stateChanged.connect(
            lambda newState: self.config.setValue(self.opt.varName, newState != Qt.CheckState.Unchecked)
        )

    def resetValue(self):
        self.checkBox.setChecked(self.config.getDefault(self.opt.varName))


class ColorField(OptionHolder):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)

        self.inputField = QLineEdit(self.config[self.opt.varName])
        self.inputField.setValidator(self.opt.validator)
        self.colorButton = QToolButton()
        self.colorButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.colorButton.clicked.connect(self.showColorPicker)
        self.inputField.setInputMask(r"\#HHHHHH")
        self.inputField.editingFinished.connect(lambda: self.setColor(self.inputField.text()))

        self.hlayout.insertItem(0, self.colorButton)
        self.hlayout.insertItem(0, self.inputField)

    def showColorPicker(self):
        """
        show a color picker when the color button is clicked.
        """
        c = QColorDialog.getColor(self.config.sLastColor, self.parent())

        if c is not None and c.isValid():
            self.setColor(c.name())

    def setColor(self, colorStr: str):
        if not colorStr:
            return
        self.inputField.setText(colorStr)
        self.colorButton.setStyleSheet(
            f"""
            QToolButton {{
                background-color: {colorStr}
            }}
            """
        )
        self.config[self.opt.varName, colorStr] = colorStr

    def resetValue(self):
        self.setColor(self.config.resetToDefault(self.opt.varName))


class IntField(OptionHolder):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)

        self.inputSlider = QSlider(Qt.Orientation.Horizontal)
        self.inputField = QLineEdit()

        val: QIntValidator = self.opt.validator

        self.inputSlider.setRange(val.bottom(), val.top())
        self.inputField.setValidator(val)

        self.inputSlider.setValue(self.config[self.opt.varName])
        self.inputField.setText(str(self.config[self.opt.varName]))

        self.inputField.editingFinished.connect(
            lambda: (
                self.inputSlider.setValue(int(self.inputField.text())),
                self.config.setValue(self.opt.varName, int(self.inputField.text())),
            )
        )

        self.sliderMoved.connect(
            lambda: (
                self.inputField.setText(str(self.inputField.text())),
                self.config.setValue(self.opt.varName, self.inputField.text()),
            )
        )

    def resetValue(self):
        val = self.config.resetToDefault(self.opt.varName)
        self.inputField.setText(str(val))
        self.inputSlider.setValue(val)

class SelectorField(OptionHolder):
    
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)
        
        self.schema : Dict[str, str] = opt.additional # in the form of {'rep name' : <val>, ...}
        self.reverse = {val:key for key, val in self.schema.items()}
        self.combo = QComboBox()
        self.combo.addItems(list(self.schema.keys()))
        self.combo.setCurrentText(str(self.reverse[self.config[self.opt.varName]]))
        self.combo.currentTextChanged.connect(lambda t:self.config.setValue(self.opt.varName, self.schema[t]))
        self.hlayout.insertItem(0, self.combo)
    
    
    def resetValue(self):
        val = self.config.resetToDefault(self.opt.varName)
        self.combo.setCurrentText(self.reverse[val])


class ConfigOptionMenu(QWidget):
    def __init__(self, parent: QWidget = None, schema: List[Option] = None):
        super().__init__(parent)
        
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        
        
        optLayout = QGridLayout()
        optLayout.setContentsMargins(0,0,0,0)

        for i, opt in enumerate(schema):
            w = None

            match opt.type:
                case OptType.intType:
                    w = IntField(opt)
                case OptType.colorType:
                    w = ColorField(opt)
                case OptType.boolType:
                    w = BoolField(opt)
                case _:
                    raise NotImplementedError()
                
            label = QLabel(opt.repName)
            label.setToolTip(opt.desc)
            
            optLayout.addWidget(label, i, 0)
            optLayout.addWidget(w, i, 1)
