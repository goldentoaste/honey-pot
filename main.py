import os
import sys
import time

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import (QGuiApplication, QImage, QTextBlock, QTextCursor,
                           QTextImageFormat)
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from GUI.mainGUI import Ui_Form
from GUI.notePreviewGUI import Ui_NotePreview


class Main(Ui_Form, QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        
        




if __name__ == "__main__":

    app = QApplication(sys.argv)
    M = Main()
    M.show()
    
    sys.exit(app.exec())
