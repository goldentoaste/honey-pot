
from PySide6.QtCore import  QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
                               QSizePolicy, QWidget)

class Divider(QWidget):
    def __init__(self, parent = None, color: QColor = Qt.GlobalColor.black, percentage=1, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(1)
        self.percentage = percentage
        self.color = color

    def paintEvent(self, event) -> None:
        p = QPainter(self)
        p.setPen(QPen(self.color, self.height()))

        h = self.height() / 2
        w = self.width() * self.percentage
        p.drawLine(QPointF(self.width() * (1 - self.percentage), h), QPointF(w, h))
        p.end()