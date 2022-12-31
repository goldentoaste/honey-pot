import os
import sys
from typing import Dict, List

if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
import json

from PySide6.QtCore import QPoint, Qt, Slot
from PySide6.QtGui import QAction, QDesktopServices, QIntValidator
from PySide6.QtWidgets import (QApplication, QCheckBox, QColorDialog,
                               QComboBox, QFileDialog, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QMenu,
                               QScrollArea, QSizePolicy, QSlider, QSpacerItem,
                               QSpinBox, QToolButton, QVBoxLayout, QWidget)

from Configs.appConfig import Option, OptType, getAppConfig
from GUI.divider import Divider
from utils import cacheLocation, copyCmd, getPath, styleLocation


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

    def update(self):
        """
        update this widget's current display value according to the config.\n
        should be used when the config has changed without the ui being changed by the user
        """
        raise NotImplementedError()


class StrField(OptionHolder):
    def __init__(self, opt: Option, *args, **kwargs) -> None:
        super().__init__(opt, *args, **kwargs)
        self.inputField = QLineEdit(self.config[self.opt.varName])
        self.hlayout.insertWidget(0, self.inputField)

    def save(self):
        self.config[self.opt.varName] = self.inputField.text()

    def resetValue(self):
        self.inputField.setText(self.config.resetToDefault(self.opt.varName))

    def update(self):
        self.inputField.setText(self.config[self.opt.varName])


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

    def update(self):
        self.checkBox.setChecked(self.config[self.opt.varName])


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

    def update(self):
        print("update color", self.opt.varName, self.config[self.opt.varName])
        self.inputField.setText(self.config[self.opt.varName])
        self.colorButton.setStyleSheet(
            f"""
            QToolButton {{
                background-color: {self.inputField.text()}
            }}
            """
        )


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

        self.inputField.valueChanged.connect(self.inputSlider.setValue)
        self.inputSlider.valueChanged.connect(lambda: (self.inputField.setValue(self.inputSlider.value())))

        self.hlayout.insertWidget(0, self.inputField)
        self.hlayout.insertWidget(0, self.inputSlider)

    def resetValue(self):
        val = self.config.resetToDefault(self.opt.varName)
        self.inputField.setValue(val)
        self.inputSlider.setValue(val)

    def save(self):
        self.config.setValue(self.opt.varName, int(self.inputField.text()))

    def update(self):
        self.inputField.setValue(self.config[self.opt.varName])


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

    def update(self):
        self.combo.setCurrentText(self.reverse[self.config[self.opt.varName]])


defaultStyles = {"Default Style": getPath("GUI\\defaultStyle.json")}


class ConfigOptionMenu(QWidget):
    def __init__(self, parent: QWidget = None, schema: List[Option] = None):
        super().__init__(parent)
        self.styles = {}
        self.parentLayout = QVBoxLayout()

        self.config = getAppConfig()

        self.setupPresets()
        self.setupOptions(schema)

    def closeEvent(self, _) -> None:
        # apply the changes when window is closed (when a preset is chosen, an update is triggered immediately)
        self.config.enableSave()
        self.config.save()
        self.config.configChanged.emit()

        for widget in self.optWidgets:
            widget.save()

    def setupPresets(self):
        self.styles: dict = {}
        self.styles.update(defaultStyles)

        self.styleLayout = QHBoxLayout()
        self.styleDropdown = QComboBox()
        self.styleDropdown.activated.connect(self.styleSelected)
        self.styleOptionButton = QToolButton()
        self.styleOptionButton.setText("...")
        self.styleOptionButton.clicked.connect(lambda: self.showPresetContext(self.styleOptionButton.pos()))
        self.styleLayout.addWidget(self.styleDropdown)
        self.styleLayout.addWidget(self.styleOptionButton)

        self.parentLayout.addLayout(self.styleLayout)

        for name, path in zip(self.config.lsSavedStyleNames, self.config.lsSavedStylePath):
            self.styles[name] = path

        self.styleDropdown.addItems(list(self.styles.keys()))
        if self.config.sCurrentStyleName:
            self.styleDropdown.setCurrentText(self.config.sCurrentStyleName)

    @Slot()
    def styleSelected(self, _):
        print("selected")
        name = self.styleDropdown.currentText()
        self.config.sCurrentStyleName = name
        path = self.styles[name]

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(name, path, data)
            content = data["content"]
            self.loadStyle(name, content)

    @Slot(QPoint)
    def showPresetContext(self, pos: QPoint):
        menu = QMenu("Menu Title")
        addNew = QAction("Add new style")
        removeCur = QAction("Remove current style")
        openFolder = QAction("Open containing folder")
        openFolder.triggered.connect(self.openStyleDir)
        addNew.triggered.connect(self.addStyle)
        removeCur.triggered.connect(self.removeCurrent)
        menu.addActions([addNew, removeCur, openFolder])
        menu.exec(self.mapToGlobal(pos))

    @Slot()
    def removeCurrent(self):
        if self.styleDropdown.currentText() in defaultStyles:
            return
        cur = self.styleDropdown.currentText()

        self.styleDropdown.setCurrentText("")

        os.remove(self.styles[cur])
        self.styles.pop(cur)

        names = self.config.lsSavedStyleNames
        paths = self.config.lsSavedStylePath

        index = names.index(cur)
        names.pop(index)
        paths.pop(index)

        self.config.lsSavedStyleNames = names
        self.config.lsSavedStylePath = paths

    @Slot()
    def addStyle(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a .json style file", filter="Json (*.json)")

        if not fileName:
            return

        with open(fileName, "r", encoding="utf-8") as f:
            data: dict = json.load(f)

            name = data["name"]

            if name in self.styles:
                return

            content: dict = data["content"]

            self.loadStyle(name, content)

            names = self.config.lsSavedStyleNames
            paths = self.config.lsSavedStylePath

            names.append(name)
            paths.append(fileName)

            self.config.lsSavedStyleNames = names
            self.config.lsSavedStylePath = paths

            self.config.save()

            self.styles[name] = fileName
            self.styleDropdown.addItem(name)
            self.styleDropdown.setCurrentText(name)

            # save a copy
            command = f'{copyCmd} "{fileName}" "{styleLocation}"'
            if sys.platform == "win32":
                command = command.replace("/", "\\")
            os.system(command)

    def loadStyle(self, name: str, content: dict = None):
        print("before", self.config.sScrollbarColor)
        self.config.setMultipleVars(content)
        print("after", self.config.sScrollbarColor)

        for widget in self.optWidgets:
            widget.update()
            print(widget)
        self.config.save()
        self.config.configChanged.emit()

        self.config.sCurrentStyleName = name

    @Slot()
    def openStyleDir(self):
        if not os.path.isdir(styleLocation):
            os.makedirs(styleLocation)
        QDesktopServices.openUrl(styleLocation)

    def setupOptions(self, schema):
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollHolder = QWidget()
        self.scrollArea.setWidget(self.scrollHolder)

        self.mainLayout = QVBoxLayout()
        self.scrollHolder.setLayout(self.mainLayout)
        self.setLayout(self.parentLayout)
        self.parentLayout.addWidget(self.scrollArea)

        sections: Dict[str, List[Option]] = {section: [] for section in self.config.getSections()}

        for opt in schema:
            sections[self.config.getSectionOfVar(opt.varName)].append(opt)

        # removing empty sections
        sections = {key: val for key, val in sections.items() if val}

        self.optWidgets: List[OptionHolder] = []

        for index, section in enumerate(sections):
            self.mainLayout.addWidget(QLabel(section))

            optLayout = QGridLayout()
            optLayout.setContentsMargins(0, 0, 0, 0)
            optLayout.setVerticalSpacing(0)
            self.mainLayout.addLayout(optLayout)
            for i, opt in enumerate(schema):
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
                self.optWidgets.append(w)

            if index < len(sections) - 1:
                self.mainLayout.addWidget(Divider())

        self.mainLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))


if __name__ == "__main__":
    from appConfig import optionSchema

    a = QApplication(sys.argv)
    w = ConfigOptionMenu(None, optionSchema)

    w.show()
    a.exec()
