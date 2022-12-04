from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent, QKeySequence
from PySide6.QtWidgets import QApplication, QLineEdit, QToolTip
import os, sys
if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
from Hotkeys.keyConsts import conversionTable

keyTextFilter= {
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
            '{':'[',
            '}':']',
            '|':'\\',
            ':':';',
            '"':"'",
            '<':',',
            '>':'.',
            '?':'/',
            '~':'`',
            "Control":'',
            "Alt":"",
            "Shift":""
        }

class KeyBindInput(QLineEdit):

    keyBindChanged = Signal(
        str, str
    )  # will emit name mapped to a Qkeysequence representing the key combo when finished editing.

    def __init__(self, parent=None, name="", keyString="", isGlobal = False):
        super().__init__(parent)
        self.isGlobal = isGlobal
        self.name = name
        self.keyString = keyString
        self.setText(keyString)
        self.original = self.keyString

    def mousePressEvent(self, arg__1) -> None:
        """
        start recording keys when this text field is clicked on.
        show a message when clicked on to give hints.
        """
        if not self.hasFocus():
            self.original = self.keyString
            print("setting focus/original")
        super().mousePressEvent(arg__1)

    def mouseReleaseEvent(self, _) -> None:
        QToolTip().showText(
            self.mapToGlobal(self.rect().topRight()),
            "Press any key combo to set key binding. \n<Esc> to cancel and keep original. \n<Enter> to confirm.",
            msecShowTime=10000,
        )

    def keyPressEvent(self, a: QKeyEvent) -> None:
        a.accept()

        if a.key() == Qt.Key.Key_Escape:
            self.keyString = self.original
            self.setText(self.original)
            self.clearFocus()
            return

        if a.key() == Qt.Key.Key_Enter:
            if self.strIsValid(self.keyString):
                self.keyBindChanged.emit(
                    self.name, self.keyString
                )
                return

        s = self.getString(a)
        if self.isGlobal:
            self.setText(s + f"({conversionTable.get(a.nativeVirtualKey())})")
        else:
            self.setText(s)
        self.keyString = s
    

    def strIsValid(self, s: str):
        out=  s.split('+')
        return len(out) > 0 and out[-1] not in ("Ctrl","Alt","Shift")

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
        return out.strip('+ ').title()
    
    def getVkName(self, vk):
        pass


if __name__ == "__main__":
    import sys

    a = QApplication(sys.argv)
    w = KeyBindInput(None, isGlobal=True)
    w.show()
    a.exec()
