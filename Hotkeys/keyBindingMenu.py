import os
import sys

from PySide6.QtCore import QObject, QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
                               QPushButton, QSizePolicy, QVBoxLayout, QWidget)

if __name__ == "__main__":
    print(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
    sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}\\.."))
from Hotkeys.hotkeyManager import HotkeyManager
from Hotkeys.keyBindInput import KeyBindInput
from Hotkeys.keyConfig import description, getKeyConfig


class Divider(QWidget):
    def __init__(self, parent, color: QColor, percentage=1, **kwargs) -> None:
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


class KeyBindingMenu(QWidget):
    def __init__(
        self,
        parent: QObject = None,
    ) -> None:
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.config = getKeyConfig()

        layout = QVBoxLayout()

        sections = self.config.getSection()
        l = len(sections)
        for i, section in enumerate(sections):

            layout.addWidget(QLabel(section))
            table = QGridLayout()
            layout.addLayout(table)
            
            index = 0

            for name, keyString in self.config.getBindings(section):
                label = QLabel(name)
                label.setToolTip(description[name])
                table.addWidget(label,
                    index, 0
                )
                

                table.addWidget(
                    KeyBindInput(None, name, keyString,  self.config.isGlobal(name)),
                    index, 1
                )
                
                index += 1

            if i < l - 1:
                layout.addWidget(Divider(None, Qt.GlobalColor.black))

        self.setLayout(layout)


if __name__ == "__main__":

    a = QApplication(sys.argv)
    w = KeyBindingMenu()
    w.show()
    a.exec()
