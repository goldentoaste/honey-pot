import os
import sys
import time

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import (QGuiApplication, QImage, QTextBlock, QTextCursor,
                           QTextImageFormat)
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from GUI.mainGUI import Ui_MainWindow
from GUI.notePreviewGUI import Ui_NotePreview


class Main(Ui_MainWindow, QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class NoteTest(Ui_NotePreview, QWidget):
    def __init__(self) -> None:
        super().__init__()

        t0 = time.time()
        self.setupUi(self)
        self.textBrowser.setStyleSheet(
            """
            QTextBrowser{
                border: 0px;
                background-color: #ffffff;
            }
            
            """
        )

        with open("test.md", "r", encoding="utf8") as f:
            self.textBrowser.setMarkdown(f.read(),)

        doc = self.textBrowser.document()

        cursor = self.textBrowser.textCursor()
        block = doc.begin()

        while block.isValid():
            bit: QTextBlock.iterator = block.begin()

            while not bit.atEnd():
                frag = bit.fragment()
                textFormat = frag.charFormat()

                # print(textFormat, textFormat.isImageFormat())

                if textFormat.isImageFormat():
                    image = textFormat.toImageFormat()
                    # print(f"Image! {image.name()}, {frag.position() , frag.length()}")

                    cursor.setPosition(frag.position(), QTextCursor.MoveAnchor)
                    cursor.setPosition(frag.position() + frag.length(), QTextCursor.KeepAnchor)
                    cursor.removeSelectedText()
                    cursor.insertImage(QImage(r"D:\PythonProject\stickyMarkdown\devineInspiration.png"), "wowies!")

                    # image.setName(r"D:\PythonProject\stickyMarkdown\devineInspiration.png")

                bit += 1
            # print("block finished, going next block")
            block = block.next()

        print("init took", time.time() - t0)

        with open("out.html", "w", encoding="utf-8") as out:
            out.write(doc.toHtml())


if __name__ == "__main__":

    app = QApplication(sys.argv)

    t = NoteTest()
    t.show()
    sys.exit(app.exec_())
