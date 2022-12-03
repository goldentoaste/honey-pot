from PySide6.QtWidgets import QLineEdit, QToolTip, QApplication
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QKeyEvent, QKeySequence
class KeyBindInput(QLineEdit):
    
    keyBindChanged = Signal(str, QKeySequence) # will emit name mapped to a Qkeysequence representing the key combo when finished editing.
    
    def __init__(self, parent = None, name ="", keyString = ""):
        super().__init__(parent)

        self.name = name
        self.keyString = keyString
        self.setText(keyString)
        self.original = self.keyString
        
    
    def mousePressEvent(self, arg__1) -> None:
        '''
        start recording keys when this text field is clicked on.
        show a message when clicked on to give hints.
        '''
        if not self.hasFocus():
            self.original = self.keyString
            print("setting focus/original")
        super().mousePressEvent(arg__1)
    
    def mouseReleaseEvent(self, _) -> None:
        QToolTip().showText(self.mapToGlobal(self.rect().topRight()),
                                    'Press any key combo to set key binding. \n<Esc> to cancel and keep original. \n<Enter> to confirm.', msecShowTime=10000)

    def keyPressEvent(self, a: QKeyEvent) -> None:
        a.accept()
        
        if a.key() == Qt.Key.Key_Escape:
            self.keyString = self.original
            self.setText(self.original)
            self.clearFocus()
            return
        
        if a.key() == Qt.Key.Key_Enter:
            if self.strIsValid(self.keyString):
                self.keyBindChanged.emit(self.name, QKeySequence(self.keyString, QKeySequence.SequenceFormat.PortableText))
        
        seq = QKeySequence( a.keyCombination())
        self.setText(self.cleanStr(seq.toString(QKeySequence.SequenceFormat.NativeText)))
        self.keyString = seq.toString(QKeySequence.SequenceFormat.PortableText)
        
        
    def strIsValid(self, s:str):
        return s not in ("Ctrl+Control","Alt+Alt", "Shift+Shift")
        
    def cleanStr(self,s:str ):
        # FIXME this is broken when ctrl, alt, shift are all pressed in certain orders.
        if s == "Ctrl+Control":
            return "Ctrl"
        if s == "Alt+Alt":
            return "Alt"
        if s == "Shift+Shift":
            return "Shift"
        return s

if __name__ ==   "__main__":
    import sys
    a = QApplication(sys.argv)
    w = KeyBindInput(None)
    w.show()
    a.exec()