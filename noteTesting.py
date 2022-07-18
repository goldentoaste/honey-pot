import sys
from typing import Dict, Tuple

from PyQt5.QtCore import QPoint, QRect, Qt, QMargins
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QApplication, QWidget

dragMargin = 8
top = 0
bot = 1
left = 2
right = 3
c = Qt.CursorShape

class ScaleableWindowFrame(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setMouseTracking(True)
        self.prevDir = (None, None)
        self.lastPos : QPoint= None

    directionCursor: Dict[Tuple[int, int], Qt.CursorShape] = {
        (top, left): c.SizeFDiagCursor,
        (top, None): c.SizeVerCursor,
        (top, right): c.SizeBDiagCursor,
        (None, left): c.SizeHorCursor,
        (None, right): c.SizeHorCursor,
        (bot, left): c.SizeBDiagCursor,
        (bot, None): c.SizeVerCursor,
        (bot, right): c.SizeFDiagCursor,
        (None, None): c.ArrowCursor,
    }

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        
        if a0.buttons() == Qt.MouseButton.LeftButton:
            self.lastPos = a0.globalPos()
        a0.accept()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if a0.buttons() == Qt.MouseButton.NoButton:
            self.handleHover(a0)
        elif a0.buttons() == Qt.MouseButton.LeftButton:
            self.handleDrag(a0)
        a0.accept()

    def handleDrag(self, a0:QMouseEvent):
        diff = a0.globalPos() - self.lastPos
        
        dx = diff.x()
        dy = diff.y()
        
        methods = {
            (top, left): lambda: (self.setGeometry(QRect(self.pos() + QPoint(dx, dy), self.size().grownBy(QMargins(0,0, -dx, -dy))))),
            (top, None): lambda: (self.setGeometry(QRect(self.pos() + QPoint(0, dy), self.size().grownBy(QMargins(0,0, 0, -dy))))) ,
            (top, right):lambda: (self.setGeometry(QRect(self.pos() + QPoint(0, dy), self.size().grownBy(QMargins(0,0, dx, -dy))))) ,
            (None, left):lambda: (self.setGeometry(QRect(self.pos() + QPoint(dx, 0), self.size().grownBy(QMargins(0, 0, -dx, 0))))),
            (None, right):lambda: (self.setGeometry(QRect(self.pos(), self.size().grownBy(QMargins(0,0, dx, 0))))),
            (bot, left): lambda: (self.setGeometry(QRect(self.pos() + QPoint(dx, 0), self.size().grownBy(QMargins(0,0, -dx, dy))))),
            (bot, None):lambda: (self.setGeometry(QRect(self.pos(), self.size().grownBy(QMargins(0,0, 0, dy))))),
            (bot, right): lambda: (self.setGeometry(QRect(self.pos(), self.size().grownBy(QMargins(0,0, dx, dy))))),
            (None, None): lambda: (),
        }
        
        methods[self.prevDir]()
        self.lastPos = a0.globalPos()
        a0.accept()
    
    def handleHover(self, a0: QMouseEvent):
        # first determine which edge the mouse cursor is on
        p = a0.pos()
        # vertical direction
        if p.y() < dragMargin:
            v = top
        elif self.height() - p.y() < dragMargin:
            v = bot
        else:
            v = None

        # horizontal direction
        if p.x() < dragMargin:
            h = left
        elif self.width() - p.x() < dragMargin:
            h = right
        else:
            h = None

        direction = (v, h)
        if direction != self.prevDir:
            self.setCursor(ScaleableWindowFrame.directionCursor[(v, h)])
            self.prevDir = direction
        a0.accept()

if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = ScaleableWindowFrame()
    w.setWindowFlag(Qt.FramelessWindowHint, True)
    w.resize(400, 400)
    w.show()
    sys.exit(a.exec())