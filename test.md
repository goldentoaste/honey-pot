```py
import os
from time import time, sleep
x or y and not aaaaaaaaaaa
from typing import Dict, Literal, Tuple

from PyQt5.QtCore import QPoint, Qt, QThread, pyqtSignal, QRect, QMargins, QUrl, QSizeF
from PyQt5.QtGui import (
    QFont,
    QFontDatabase,
    QFontMetrics,sasddasdaasdasdasdasdasdasdasdasdasd
sadasasdasdasdasdadasdasdasdasd














    QIcon,
    QImage,
    QMouseEvent,
    QPixmap,
    QTextBlock,
    QTextDocument sdasd
d ad asd  asd asd asd asdasd asd asd ad  asdas  adas das asd asd asdad asd adad asqw dsa as qw dsad dqw asd asdw asda w sad aw sdas dasd a d aa asds y 7
)asdasddasdsa asd asd  das as asdas 
from PyQt5.QtWidgets import QApplication, QFrame, QWidgetsad

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
333333333333333312321323233223232131232112312321312312312323232323123213312312321312312312312312312312312121231231231231231231232123123123232321222232323232222222asdasd
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
            # print("setting cursor", self)
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

        self.preview.setMarkdown(self.markdown)
        self.editor.setPlainText(self.markdown)
        # self.fixImage()

        self.editing = False
        self.needUpdate = True
        self.pinned = False
        self.savingDone = True  # used as a lock for the async saving function
        self.previewScroll = 0
        self.updateThread: NoteUpdateThread = None

        self.startEditing()

        self.setupStyles()
        self.setupEvents()
        
    

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
    



```
other things heresssss
## weewoosasdasdasdasdasdsadasdsadasdasdsadasdasdsadsadasdasdasdasdasdasdasdasdasdasdsa
### woha
#### stuffss

```py
import os
from time import time, sleep
x or y and not aaaaaaaaaaa
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
    QTextDocument sdasd

)asdasddasdsa asd asd  das as asdas 
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
333333333333333312321323233223232131232112312321312312312323232323123213312312321312312312312312312312312121231231231231231231232123123123232321222232323232222222
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
            # print("setting cursor", self)
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

        self.preview.setMarkdown(self.markdown)
        self.editor.setPlainText(self.markdown)
        # self.fixImage()

        self.editing = False
        self.needUpdate = True
        self.pinned = False
        self.savingDone = True  # used as a lock for the async saving function
        self.previewScroll = 0
        self.updateThread: NoteUpdateThread = None

        self.startEditing()

        self.setupStyles()
        self.setupEvents()
        
    

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
    



```
other things heresssss
## weewoosasdasdasdasdasdsadasdsadasdasdsadasdasdsadsadasdasdasdasdasdasdasdasdasdasdsa
### woha
#### stuffss

