from PySide6.QtWidgets import QApplication, QWidget


import ctypes
import os
from threading import Thread
from time import sleep, time
from typing import Dict, Literal, Tuple

from PySide6.QtCore import (QEvent, QMargins, QPoint, QRect, QSizeF, Qt, 
                            QThread, QUrl, Signal)
from PySide6.QtGui import (QFont, QFontDatabase, QFontMetrics, QIcon, QImage, QCursor,
                           QMouseEvent, QPixmap, QTextBlock, QTextDocument, QShortcut, QKeySequence)
from PySide6.QtWidgets import QApplication, QFrame, QWidget

# from GUI.noteGUI import Ui_Note
# from imageCache import CacheManager
# from utils import  getPath
# import sys
# from Hotkeys.keyConfig import getKeyConfig
# user32 = ctypes.windll.user32

import sys
if __name__ == '__main__':
    a = QApplication(sys.argv)
    
    w = QWidget()
    w.show()
    a.exec()