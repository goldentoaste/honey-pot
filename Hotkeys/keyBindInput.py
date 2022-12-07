import os
import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent, QKeySequence
from PySide6.QtWidgets import QApplication, QLineEdit, QToolTip,QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy

if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
from Hotkeys.keyConsts import conversionTable
from Hotkeys.keyConfig import getKeyConfig




keyTextFilter = {
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "_": "-",
    "+": "=",
    "{": "[",
    "}": "]",
    "|": "\\",
    ":": ";",
    '"': "'",
    "<": ",",
    ">": ".",
    "?": "/",
    "~": "`",
    "Control": "",
    "Alt": "",
    "Shift": "",
}


class KeyBindInput(QWidget):


    def __init__(self, parent=None, name="", keyString="", isGlobal=False):
        super().__init__(parent)
        self.isGlobal = isGlobal
        self.name = name
        self.keyString = keyString
        
        self.config = getKeyConfig()
        
        layout = QHBoxLayout()
      
        self.lineEdit = QLineEdit()      
        self.lineEdit.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Maximum)
        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.reset)
        self.resetButton.setMinimumWidth(1)
        self.resetButton.setSizePolicy(QSizePolicy.Policy.Maximum,QSizePolicy.Policy.Maximum)

        layout.addWidget(self.lineEdit)
        layout.addWidget(self.resetButton)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        
        self.lineEdit.mousePressEvent = self._mousePressEvent
        self.lineEdit.mouseReleaseEvent = self._mouseReleaseEvent 
        self.lineEdit.keyPressEvent = self._keyPressEvent
        
        self.lineEdit.setText(keyString)
        self.original = self.keyString
        
    def reset(self):
        newstr = self.config.resetBinding(self.name)
        self.keyString = newstr
        self.lineEdit.setText(newstr)
        

    def _mousePressEvent(self, arg__1) -> None:
        """
        start recording keys when this text field is clicked on.
        show a message when clicked on to give hints.
        """
        if not self.lineEdit.hasFocus():
            self.original = self.keyString
            print("setting focus/original")
        QLineEdit.mousePressEvent(self.lineEdit,arg__1)

    def _mouseReleaseEvent(self, _) -> None:
        QToolTip().showText(
            self.mapToGlobal(self.lineEdit.rect().topRight()),
            "Press any key combo to set key binding. \n<Esc> to cancel and keep original. \n<Enter> to confirm.",
            msecShowTime=10000,
        )

    def _keyPressEvent(self, a: QKeyEvent) -> None:
        a.accept()
        
        print("help", a.key(), a.key()==Qt.Key.Key_Return,  a.key()==Qt.Key.Key_Enter)
        if a.key() == Qt.Key.Key_Escape:
            self.keyString = self.original
            self.lineEdit.setText(self.original)
            self.clearFocus()
            return

        if  a.key()==Qt.Key.Key_Return or a.key() == Qt.Key.Key_Enter:
            if self.strIsValid(self.keyString):
                if self.isGlobal:
                    self.config.updateGlobalBinding(self.name, self.keyString)
                else:
                    self.config.updateBinding(self.name, QKeySequence(self.keyString))
                return

        s = self.getString(a)
        if self.isGlobal:
            self.lineEdit.setText(s + f"({conversionTable.get(a.nativeVirtualKey())})")
        else:
            self.lineEdit.setText(s)
        self.keyString = s

    def strIsValid(self, s: str):
        out = s.split("+")
        return len(out) > 0 and out[-1] not in ("Ctrl", "Alt", "Shift")

    def getString(self, a: QKeyEvent):
        out = ""

        if a.modifiers() & Qt.KeyboardModifier.ControlModifier:
            out += "Ctrl+"
        if a.modifiers() & Qt.KeyboardModifier.AltModifier:
            out += "Alt+"
        if a.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            out += "Shift+"

        if not self.isGlobal:
            t = QKeySequence(a.key()).toString()

            out += keyTextFilter.get(t, t)
        else:
            out += str(a.nativeVirtualKey())
        return out.strip("+ ").title()


if __name__ == "__main__":
    import sys

    a = QApplication(sys.argv)
    w = KeyBindInput(None, isGlobal=False)
    w.show()
    a.exec()
