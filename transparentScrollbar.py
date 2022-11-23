

from PySide6.QtWidgets import QScrollBar, QWidget, QScrollArea
from PySide6.QtCore import QRect, QSize, Qt, Signal, Slot
from PySide6.QtGui import QPaintEvent, QPainter, QPen, QBrush, QColor


class ScrollProxy(QScrollBar):
    changedSignal = Signal(QScrollBar.SliderChange)
    
    def sliderChange(self, change) -> None:
        self.changedSignal.emit(change)
        super().sliderChange(change)
    
    
class TransScrollBar(QWidget):
    
    def __init__(self, orient : Qt.Orientation,  parent : QWidget, scrollArea: QScrollArea) -> None:
        super().__init__(parent)
        self.scrollArea = scrollArea
        self.orientation = orient
        self.proxy = ScrollProxy(self.orientation)
        self.proxy.changedSignal.connect(self.barChanged)
        if orient == Qt.Orientation.Vertical:
            scrollArea.setVerticalScrollBar(self.proxy)
            scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            
            scrollArea.setHorizontalScrollBar(self.proxy)
            scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
     
    
    @Slot(QScrollBar.SliderChange)
    def barChanged(self, change : QScrollBar.SliderChange):
        print("fdmfsdkmdsmfdm", change)
        
    
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
        
    def sliderChange(self, change) -> None:
        print("hlgpeghlelpfge", change)
        
        

    def mousePressEvent(self, event) -> None:
        
        print(event.position())
        event.accept()