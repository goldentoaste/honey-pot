

from PySide6.QtWidgets import QScrollBar, QWidget
from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QPaintEvent, QPainter, QPen, QBrush, QColor
class TransScrollBar(QWidget):
    
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.resize(400, 400)
    
    def sizeHint(self):
        return QSize(400,400)
    
    
    def paintEvent(self, arg:QPaintEvent) -> None:

        painter  = QPainter(self)
        
        pen= QPen(QColor("#ffffff"), 0)
        brush  = QBrush(QColor("#ff0000"))
        
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(QRect(0, 0, 100, 100))
        
        painter.end()