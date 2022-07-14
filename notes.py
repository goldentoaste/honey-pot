from PyQt5.QtWidgets import QWidget, QApplication, QFrame

from GUI.noteGUI import Ui_Note
from PyQt5.QtCore import Qt, QThread, pyqtSignal

import os
from PyQt5.QtGui import QTextBlock, QTextCursor, QImage, QFont, QFontDatabase, QFontMetrics, QIcon, QPixmap, QMouseEvent

from imageCache import CacheManager

import time
from utils import getResource

updateInterval = 1


class Note(Ui_Note, QWidget):
    def __init__(
        self,
        filePath: str,
        cacheManager: CacheManager,
        markdown: str = None,
    ) -> None:
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.cacheManager = cacheManager
        if not os.path.isfile(filePath):
            with open(filePath, "w", encoding="utf8") as _:
                # create a empty file
                markdown = ""

        if markdown:
            self.markdown = markdown
        else:
            with open(filePath, "r", encoding="utf8") as f:
                self.markdown = f.read()

        self.preview.setMarkdown(self.markdown)
        self.editor.setText(self.markdown)
        self.fixImage()

        self.editing = False
        self.needUpdate = True
        self.previewScroll = 0
        self.updateThread: NoteUpdateThread = None
        self.startEditing()

        self.setupStyles()
        self.setupEvents()

    def setupEvents(self):
        self.setMouseTracking(True)
        self.editor.textChanged.connect(lambda: setattr(self, 'needUpdate', True))
        self.closeButton.clicked.connect(self.close)
        self.minimizeButton.clicked.connect(lambda:self.setWindowState(Qt.WindowState.WindowMinimized))
        
    
    def setupStyles(self):
        # fonts stuff
        QFontDatabase.addApplicationFont(r"GUI/Raleway-Light.ttf")
        font = QFont()
        font.setFamily("Raleway")
        print(QFont.Weight.Black)
        font.setWeight(35)
        font.setPointSize(11)
        self.previewFont = font
        self.preview.setFont(self.previewFont)

        self.editorFont = QFont("Cascadia Code", 9, QFont.Weight.Light)
        self.editor.setFont(self.editorFont)

        metric = QFontMetrics(self.editorFont)
        self.editor.setTabStopDistance(metric.width(" ") * 4)

        # button icons
        self.pinIcon = QIcon(QPixmap(getResource("GUI\\pin.svg")))
        self.filledPinIcon = QIcon(QPixmap(getResource("GUI\\pinFilled.svg")))

        self.pinButton.setIcon(self.pinIcon)
        self.newNoteButton.setIcon(QIcon(QPixmap(getResource("GUI\\add.svg"))))
        self.editButton.setIcon(QIcon(QPixmap(getResource("GUI\\edit.svg"))))
        self.minimizeButton.setIcon(QIcon(QPixmap(getResource("GUI\\minimize.svg"))))
        self.closeButton.setIcon(QIcon(QPixmap(getResource("GUI\\close.svg"))))

    def updatePreview(self):
        if self.editing and self.needUpdate:
            self.previewScroll = self.preview.verticalScrollBar().value()
            self.preview.setMarkdown(self.editor.toPlainText())
            self.fixImage()
            self.needUpdate = False
            self.preview.verticalScrollBar().setValue(self.previewScroll)

    def startEditing(self):

        if not self.updateThread:
            self.updateThread = NoteUpdateThread(self)
        self.updateThread.updateSignal.connect(self.updatePreview)
        self.updateThread.start()
        self.editing = True

    def stopEditing(self):
        self.updateThread.stop()
        self.editing = False

    def close(self) -> bool:
        if self.updateThread:
            self.updateThread.stop()
        return super().close()

    def fixImage(self):
        """
        searched for images found in parsed documents
        replace web images with cached local images
        already local images are ignored.
        """
        doc = self.preview.document()
        cursor = self.preview.textCursor()

        block = doc.begin()

        while block.isValid():
            bit = QTextBlock.iterator = block.begin()

            while not bit.atEnd():
                fragment = bit.fragment()
                textFormat = fragment.charFormat()

                if textFormat.isImageFormat():
                    imageFormat = textFormat.toImageFormat()

                    imagePath = imageFormat.name()
                    if not os.path.isfile(imagePath):
                        cachedWebFile = self.cacheManager.getFile(imagePath)

                        if cachedWebFile:
                            cursor.setPosition(fragment.position(), QTextCursor.MoveAnchor)
                            cursor.setPosition(fragment.position() + fragment.length(), QTextCursor.KeepAnchor)
                            cursor.removeSelectedText()
                            cursor.insertImage(QImage(cachedWebFile), imagePath)
                bit += 1
            block = block.next()

class DraggableFrameBar:
    
    def __init__(self, frame:QFrame) -> None:
        self.parent = frame.parent()
        self.frame = frame
        frame.setMouseTracking(True)
        frame.mousePressEvent = self.mousePressEvent
        frame.mouseMoveEvent = self.mouseMoveEvent
        frame.mouseReleaseEvent = self.mouseReleaseEvent
    
    def mousePressEvent(self, a0: QMouseEvent):
        pass
    
    def mouseMoveEvent(self, a0:QMouseEvent):
        pass
    
    def mouseReleaseEvent(self, a0:QMouseEvent):
        pass

class NoteUpdateThread(QThread):
    updateSignal = pyqtSignal()

    def __init__(self, parent: Note = None) -> None:
        super().__init__(parent)
        self.shouldRun = True

    def stop(self):
        self.shouldRun = False

    def run(self) -> None:
        while self.shouldRun:
            self.updateSignal.emit()
            time.sleep(updateInterval)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    from qt_material import apply_stylesheet

    # apply_stylesheet(app, theme='GUI/colors.xml')

    with open("test.md", "r", encoding="utf8") as f:
        n = Note(
            r"D:\PythonProject\stickyMarkdown\test.md",
            CacheManager(r"D:\PythonProject\stickyMarkdown\testCache", 5),
            f.read(),
        )

    n.show()
    sys.exit(app.exec_())
