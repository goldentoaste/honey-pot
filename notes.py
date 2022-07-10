from PyQt5.QtWidgets import QWidget, QApplication

from GUI.noteGUI import Ui_Note
from PyQt5.QtCore import Qt

import os


class Note(Ui_Note, QWidget):
    def __init__(self, filePath:str,  markdown:str = None) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        
        if not os.path.isfile():
            with open(filePath, 'w', encoding='utf8') as _:
                # create a empty file
                markdown = ""
        
        if markdown:
            self.markdown = markdown
        else:
            with open(filePath, 'r', encoding='utf8') as f:
                self.markdown = f.read()
        
    
    
    def setMarkdown(self):
        self.preview.setMarkdown(self.markdown)
    
    def fixImage(self):
        pass



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    from qt_material import apply_stylesheet
    apply_stylesheet(app, theme='GUI/colors.xml')
    
    with open('test.md', 'r', encoding= 'utf8') as f:
        
        n = Note(f.read())

    n.show()
    sys.exit(app.exec_())
