from typing import Dict, List
import sys, os

if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (QCheckBox, QColorDialog, QComboBox, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
                               QSlider, QToolButton, QVBoxLayout, QWidget, QApplication, QSpinBox, QSpacerItem)

from Configs.appConfig import Option, OptType, getAppConfig
from GUI.divider import Divider
import sys

class OptionHolder(QWidget):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.contentChanged = False
        self.opt = opt
        self.config = getAppConfig()

        self.hlayout = QHBoxLayout()

        self.resetButton = QToolButton()
        self.resetButton.setText("Reset")
        self.resetButton.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
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

    def save(self):
        raise NotImplementedError()


class StrField(OptionHolder):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)

        self.inputField = QLineEdit(self.config[self.opt])
        self.hlayout.insertWidget(0,self.inputField)

    def save(self):
        self.config[self.opt.varName] = self.inputField.text()


class BoolField(OptionHolder):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)

        self.checkBox = QCheckBox()
        self.checkBox.setChecked(self.config[self.opt.varName])  # pray the type matches
        self.hlayout.insertWidget(0, self.checkBox)

    def resetValue(self):
        self.checkBox.setChecked(self.config.getDefault(self.opt.varName))

    def save(self):
        self.config.setValue(self.opt.varName, self.checkBox.checkState() != Qt.CheckState.Unchecked)


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

        self.hlayout.insertWidget(0, self.colorButton)
        self.hlayout.insertWidget(0, self.inputField)
        
        self.setColor(self.inputField.text())

    def showColorPicker(self):
        """
        show a color picker when the color button is clicked.
        """
        c = QColorDialog.getColor(self.inputField.text(), self.parent())

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

    def save(self):
        self.config[self.opt.varName] = self.inputField.text()

    def resetValue(self):
        self.setColor(self.config.resetToDefault(self.opt.varName))


class IntField(OptionHolder):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)

        self.inputSlider = QSlider(Qt.Orientation.Horizontal)
        self.inputField = QSpinBox()
        
    
        val: QIntValidator = self.opt.validator

        self.inputSlider.setRange(val.bottom(), val.top())
        self.inputField.setMaximum(val.top())
        self.inputField.setMinimum(val.bottom())

        self.inputSlider.setValue(self.config[self.opt.varName])
        self.inputField.setValue(self.config[self.opt.varName])

        self.inputField.editingFinished.connect(lambda: (self.inputSlider.setValue(self.inputField.value())))

        self.inputSlider.sliderMoved.connect(lambda: (self.inputField.setValue(self.inputSlider.value())))
        
        self.hlayout.insertWidget(0,self.inputField)
        self.hlayout.insertWidget(0,self.inputSlider)
        

    def resetValue(self):
        val = self.config.resetToDefault(self.opt.varName)
        self.inputField.setValue(val)
        self.inputSlider.setValue(val)

    def save(self):
        self.config.setValue(self.opt.varName, int(self.inputField.text()))


class SelectorField(OptionHolder):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)

        self.schema: Dict[str, str] = opt.additional  # in the form of {'rep name' : <val>, ...}
        self.reverse = {val: key for key, val in self.schema.items()}
        self.combo = QComboBox()
        self.combo.addItems(list(self.schema.keys()))
        self.combo.setCurrentText(str(self.reverse[self.config[self.opt.varName]]))
        self.hlayout.insertWidget(0, self.combo)

    def resetValue(self):
        val = self.config.resetToDefault(self.opt.varName)
        self.combo.setCurrentText(self.reverse[val])

    def save(self):
        self.config.setValue(self.opt.varName, self.schema[self.combo.currentText()])


class ConfigOptionMenu(QWidget):
    def __init__(self, parent: QWidget = None, schema: List[Option] = None):
        super().__init__(parent)

        mainLayout = QVBoxLayout()
        # mainLayout.setContentsMargins(0, 0, 0, 0)

        # divide to each section

        self.config = getAppConfig()
        sections: Dict[str, List[Option]] = {section: [] for section in self.config.getSections()}
        
        print(sections)
        print("----")
        for opt in schema:
            print(self.config.getSectionOfVar(opt.varName))
            sections[self.config.getSectionOfVar(opt.varName)].append(opt)

        # removing empty sections
        sections = {key : val for key,val in sections.items() if val}

        self.optWidgets: List[OptionHolder] = []

        for index, section in enumerate(sections):
            mainLayout.addWidget(QLabel(section))

            optLayout = QGridLayout()
            optLayout.setContentsMargins(0, 0, 0, 0)
            optLayout.setVerticalSpacing(0)
            mainLayout.addLayout(optLayout)
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

            if index < len(sections)-1:
                mainLayout.addWidget(Divider())
            
        mainLayout.addItem(QSpacerItem(0,0,QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding ))
        self.setLayout(mainLayout)
        
if __name__ == '__main__':
    from appConfig import optionSchema
    a = QApplication(sys.argv)
    w = ConfigOptionMenu(None, optionSchema)
    
    w.show()
    a.exec()
