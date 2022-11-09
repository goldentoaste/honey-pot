import os
from time import time, sleep

from typing import Dict, Literal, Tuple

from PyQt5.QtCore import QPoint, Qt, QThread, pyqtSignal, QRect, QMargins, QUrl, QSizeF
from PyQt5.QtGui import (
    QFont,
    QFontDatabase,
    QFontMetrics,
    QIcon,
    QImage,
    QMouseEvent,
    QPixmap,
    QTextBlock,
    QTextDocument

)
from PyQt5.QtWidgets import QApplication, QFrame, QWidget

from GUI.noteGUI import Ui_Note
from imageCache import CacheManager
from utils import getResource
from threading import Thread
import ctypes

user32 = ctypes.windll.user32

updateInterval = 1
ignoreMargin = 12
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
        self.lastPos: QPoint = None

        # user32.SetWindowLongPtrA(
        #     int(self.winId()),
        #     -16,
        #     0x00840000,
        # )
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

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

    def handleDrag(self, a0: QMouseEvent):
        if not self.lastPos:
            return
        diff = a0.globalPos() - self.lastPos

        dx = diff.x()
        dy = diff.y()

        methods = {
            (top, left): lambda: (
                self.setGeometry(
                    QRect(self.pos() + QPoint(dx, dy), self.size().grownBy(QMargins(0, 0, -dx, -dy)))
                )
            ),
            (top, None): lambda: (
                self.setGeometry(
                    QRect(self.pos() + QPoint(0, dy), self.size().grownBy(QMargins(0, 0, 0, -dy)))
                )
            ),
            (top, right): lambda: (
                self.setGeometry(
                    QRect(self.pos() + QPoint(0, dy), self.size().grownBy(QMargins(0, 0, dx, -dy)))
                )
            ),
            (None, left): lambda: (
                self.setGeometry(
                    QRect(self.pos() + QPoint(dx, 0), self.size().grownBy(QMargins(0, 0, -dx, 0)))
                )
            ),
            (None, right): lambda: (
                self.setGeometry(QRect(self.pos(), self.size().grownBy(QMargins(0, 0, dx, 0))))
            ),
            (bot, left): lambda: (
                self.setGeometry(
                    QRect(self.pos() + QPoint(dx, 0), self.size().grownBy(QMargins(0, 0, -dx, dy)))
                )
            ),
            (bot, None): lambda: (
                self.setGeometry(QRect(self.pos(), self.size().grownBy(QMargins(0, 0, 0, dy))))
            ),
            (bot, right): lambda: (
                self.setGeometry(QRect(self.pos(), self.size().grownBy(QMargins(0, 0, dx, dy))))
            ),
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
        if p.x() <= dragMargin:
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


def ignoreEdgeDrag(target: QWidget, parent: QWidget, borderSize: int):

    oldPressEvent = target.mousePressEvent
    oldMoveEvent = target.mouseMoveEvent
    oldReleaseEvent = target.mouseReleaseEvent
    target.ignoring = False
    
    target.setMouseTracking(True)

    def makeReplacementEvent(eventType: Literal["press", "move", "release"]):
        # false for press event
        def replacementEvent(event: QMouseEvent):
            # FIXME maybe split this to 3 functions instead
            if eventType == "release":
                if target.ignoring:
                    target.ignoring = False
                    event.ignore()
                    return
            if target.ignoring:
                event.ignore()
                return

            mX = event.globalX()
            mY = event.globalY()

            pX0 = parent.x()
            pY0 = parent.y()
            pX1 = pX0 + parent.width()
            pY1 = pY0 + parent.height()

            # within margin
            if any(
                (mX - pX0 <= borderSize, mY - pY0 <= borderSize, pX1 - mX < borderSize, pY1 - mY < borderSize)
            ):
                event.ignore()
                if eventType == "press":
                    target.ignoring = True
                return

            if eventType == "press":
                return oldPressEvent(event)
            elif eventType == "move":
                return oldMoveEvent(event)
            else:
                return oldReleaseEvent(event)

        return replacementEvent

    target.mousePressEvent = makeReplacementEvent(eventType="press")
    target.mouseMoveEvent = makeReplacementEvent(eventType="move")
    target.mouseReleaseEvent = makeReplacementEvent(eventType="release")


def ignoreHover(ob: QWidget) -> QWidget:
    ob.setMouseTracking(True)
    evt = ob.mouseMoveEvent
    # ob.mouseMoveEvent = lambda a0: a0.ignore()
    ob.mouseMoveEvent = lambda a0: (a0.ignore() if a0.buttons() == Qt.MouseButton.NoButton else evt(a0))


class Note(Ui_Note, ScaleableWindowFrame):
    def __init__(
        self,
        filePath: str,
        cacheManager: CacheManager,
        markdown: str = None,
    ) -> None:
        super().__init__()
        self.setupUi(self)
        self.cacheManager = cacheManager
        self.filePath = filePath
        if not os.path.isfile(filePath):
            with open(filePath, "w", encoding="utf8") as _:
                # create a empty file
                markdown = ""

        if markdown:
            self.markdown = markdown
        else:
            with open(filePath, "r", encoding="utf8") as f:
                self.markdown = f.read()

        
        self.editor.setPlainText(self.markdown)
        # self.fixImage()

        self.editing = False
        self.needUpdate = True
        self.pinned = False
        self.savingDone = True  # used as a lock for the async saving function
        self.previewScroll = 0
        self.updateThread: NoteUpdateThread = None
        self.sizeAdjustTimer = - 1

        self.startEditing()

        self.setupStyles()
        self.setupEvents()
        
        self.preview.setReadOnly(True)
        self.preview.setUndoRedoEnabled(False)
        self.preview.setAcceptRichText(False)

    

    def setupEvents(self):
        self.setMouseTracking(True)
        self.editor.textChanged.connect(lambda: setattr(self, "needUpdate", True))
        self.closeButton.clicked.connect(self.close)
        self.minimizeButton.clicked.connect(lambda: self.setWindowState(Qt.WindowState.WindowMinimized))
        makeFrameDraggable(self.frame)
        ignoreEdgeDrag(self.frame, self, ignoreMargin)
        ignoreEdgeDrag(self.pinButton, self, ignoreMargin)
        ignoreEdgeDrag(self.newNoteButton, self, ignoreMargin)
        ignoreEdgeDrag(self.editButton, self, ignoreMargin)
        ignoreEdgeDrag(self.minimizeButton, self, ignoreMargin)
        ignoreEdgeDrag(self.closeButton, self, ignoreMargin)
        ignoreEdgeDrag(self.editLabel, self,ignoreMargin)
        ignoreEdgeDrag(self.previewLabel, self, ignoreMargin)
        
        # x = (ignoreHover(item) for item in (self.pinButton, self.newNoteButton, self.editButton, self.minimizeButton, self.closeButton, self.frame))
    

    
    def setupStyles(self):
        # fonts stuff
        QFontDatabase.addApplicationFont(r"GUI/Roboto-Regular.ttf")
        font = QFont()
        font.setFamily("Roboto")

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

        self.pinButton.clicked.connect(self.togglePin)
        self.editButton.clicked.connect(self.toggleEdit)

    def toggleEdit(self):
        if self.editing:
            self.stopEditing()
            self.editor.hide()
            self.editLabel.hide()
            self.previewLabel.hide()
        else:
            self.startEditing()
            self.editor.show()
            self.editLabel.show()
            self.previewLabel.show()

    def saveContent(self):
        """
        saves the markdown content to disk
        this shouldnt be called too often since it must rewrite the entire file
        """

        def save():
            self.savingDone = False
            with open(self.filePath, "w", encoding="utf-8") as f:
                f.write(self.markdown)
            self.savingDone = True

        if not self.savingDone:
            return
        
        self.savingThread = Thread(target=save)
        self.savingThread.start()

    def togglePin(self):
        if self.pinned:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
            self.pinButton.setIcon(self.pinIcon)
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.pinButton.setIcon(self.filledPinIcon)
        self.pinned = not self.pinned
        self.show()

    def updatePreview(self):

        if self.editing and self.needUpdate:
            
            self.sizeAdjustTimer = 2
            
            t0 = time()
            self.previewScroll = self.preview.verticalScrollBar().value()
            self.markdown = self.editor.toPlainText()
            self.preview.setMarkdown(self.markdown)
            # self.preview.document().adjustSize()
            # self.fixImage()
            self.needUpdate = False
            self.preview.verticalScrollBar().setValue(self.previewScroll)
 
            self.saveContent()
            print(f"update took {time()-t0}")
        
        if self.sizeAdjustTimer > 0:
            self.sizeAdjustTimer -= 1
        elif self.sizeAdjustTimer > -999:
            if self.preview.document().idealWidth()>= self.preview.width():
                self.preview.document().adjustSize()
            
            self.sizeAdjustTimer = -1000
            
    def resizeEvent(self, a0) -> None:
        
        self.sizeAdjustTimer = 1

    def startEditing(self):

        if not self.updateThread:
            self.updateThread = NoteUpdateThread(self)
        self.updateThread.updateSignal.connect(self.updatePreview)
        self.updateThread.start()
        self.editing = True

    def stopEditing(self):
        # self.updateThread.stop()
        self.editing = False

    def closeEvent(self, evt) -> bool:
        self.saveContent()
        if self.updateThread:
            self.updateThread.stop()
            self.updateThread.terminate()

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
                            self.preview.document().addResource(2, QUrl(imagePath), QImage(r"D:\PythonProject\stickyMarkdown\testCache\2e53f07491fb7dc99e3aa8d9c9b4c8a9.png"))
                            print(self.preview.document().resource(2, QUrl(imagePath),))
                            print(self.preview.document().resource(2, QUrl("stufgf"),))
                            # self.preview.loadResource(2, QUrl(cachedWebFile))
                            # self.preview.viewport().update()
                            # cursor.setPosition(fragment.position(), QTextCursor.MoveAnchor)
                            # cursor.setPosition(
                            #     fragment.position() + fragment.length(), QTextCursor.KeepAnchor
                            # )
                            # cursor.removeSelectedText()
                            # cursor.insertImage(QImage(cachedWebFile), imagePath)
                bit += 1
            block = block.next()


def makeFrameDraggable(frame: QFrame):

    frame.setMouseTracking(True)
    frame.offset = None

    def mousePressEvent(a0: QMouseEvent):
        frame.offset = a0.screenPos() - frame.mapToGlobal(frame.pos())

    def mouseMoveEvent(a0: QMouseEvent):
        if frame.offset:
            frame.parent().move((a0.screenPos() - frame.offset).toPoint())

    def mouseExitEvent(_: QMouseEvent):

        frame.offset = None

    def mouseReleaseEvent(_: QMouseEvent):
        frame.offset = None

    frame.mousePressEvent = mousePressEvent
    frame.mouseMoveEvent = mouseMoveEvent
    frame.mouseReleaseEvent = mouseReleaseEvent
    frame.leaveEvent = mouseExitEvent


class NoteUpdateThread(QThread):
    updateSignal = pyqtSignal()

    def __init__(self, parent: Note = None) -> None:
        super().__init__(parent)
        self.shouldRun = True

    def start(self) -> None:
        self.shouldRun = True
        return super().start()

    def stop(self):
        self.shouldRun = False

    def run(self) -> None:
        while self.shouldRun:
            self.updateSignal.emit()
            sleep(updateInterval)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # from qt_material import apply_stylesheet

    # apply_stylesheet(app, theme='GUI/colors.xml')

    n = Note(
            r"D:\PythonProject\stickyMarkdown\test.md",
            CacheManager(r"D:\PythonProject\stickyMarkdown\testCache", 5),
           "",
        )

    # with open("test.md", "r", encoding="utf8") as f:
    #     n = Note(
    #         r"D:\PythonProject\stickyMarkdown\test.md",
    #         CacheManager(r"D:\PythonProject\stickyMarkdown\testCache", 5),
    #         f.read(),
    #     )

    n.show()
    sys.exit(app.exec_())
