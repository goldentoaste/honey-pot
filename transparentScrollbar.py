from PySide6.QtCore import QPoint, QRect, QSize, Qt, Signal, Slot
from PySide6.QtGui import QBrush, QColor, QPainter, QPaintEvent, QPen
from PySide6.QtWidgets import QScrollArea, QScrollBar, QWidget


class ScrollProxy(QScrollBar):
    changedSignal = Signal(QScrollBar.SliderChange)

    def sliderChange(self, change) -> None:
        self.changedSignal.emit(change)
        super().sliderChange(change)


class TransScrollBar(QWidget):
    def __init__(self, orient: Qt.Orientation, parent: QWidget, scrollArea: QScrollArea) -> None:
        super().__init__(parent)
        self.scrollArea = scrollArea
        self.orientation = orient
        self.isVert = orient == Qt.Orientation.Vertical

        self.proxy = ScrollProxy(self.orientation)
        # replace the original scrollbars with these proxy to intercept size change events
        if orient == Qt.Orientation.Vertical:
            scrollArea.setVerticalScrollBar(self.proxy)
            scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        else:
            scrollArea.setHorizontalScrollBar(self.proxy)
            scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # scrollbar state keeping
        self.value = 0  # current pos of bar, in actual render pixel val
        self.stepSize = 0  # cur size of bar, in actual render pixel height/width
        self.minStepSize = 30
        self.barWidth = 20
        self.range = 1  # total length of the scroll content, in document pixel
        self.displayRange = 1

        self.fade = 1  # 1 for fully opaque, 0 for transparent

        self.clicked = False  # ignore val change siognal if user is dragging
        self.lastPos = None  # used to track change in bar pos
        self.clickedOut = False  # for when clicked outside of bar, teleport it

        # bind these events last, after all the vars are initialized, to avoid async madness
        self.proxy.changedSignal.connect(self.barChanged)
        parent.resizeEvent = (
            lambda originalResize: (lambda event: (originalResize(event), self.parentResized(event)))
        )(parent.resizeEvent)

    def parentResized(self, event):
        self.resize(self.sizeHint())
        if self.isVert:
            self.move(self.parent().width() - self.barWidth, 0)
        else:
            self.move(0, self.parent().height() - self.barWidth)

    def barRect(self):
        """
        used for check if mouse is in the bar
        """
        if self.isVert:
            return QRect(0, self.value, self.barWidth, self.stepSize)
        return QRect(self.value, 0, self.stepSize, self.barWidth)

    def updateValue(self):
        self.value = int(
            (self.proxy.value() / (self.range))
            * ((self.height() if self.isVert else self.width()) - self.stepSize)
        )

    @Slot(QScrollBar.SliderChange)
    def barChanged(self, change: QScrollBar.SliderChange):
        """
        when the scrollbar changes range or size, update
        """
        if not self.clicked and change == QScrollBar.SliderChange.SliderValueChange:
            self.updateValue()
        elif change == QScrollBar.SliderChange.SliderRangeChange:
            self.range = self.proxy.maximum() - self.proxy.minimum() + 1
            self.stepSize = int(
                (self.proxy.pageStep() / self.range) * (self.height() if self.isVert else self.width())
            )
            self.displayRange = (self.height() if self.isVert else self.width()) - self.stepSize
            self.updateValue()
            self.repaint()

        # comment out sliderstepsize change for, step change iff range change
        # elif change == QScrollBar.SliderChange.SliderStepsChange:
        #     print("step", self.proxy.pageStep())
        #     self.stepSize = int((self.proxy.pageStep() / self.range) * (self.height() if self.isVert else self.width()))

    def sizeHint(self):
        if self.orientation == Qt.Orientation.Vertical:
            return QSize(self.barWidth, self.parent().height())
        return QSize(
            self.parent().width() - self.barWidth, self.barWidth
        )  # hor bar should always yield to vert bar

    def paintEvent(self, arg: QPaintEvent) -> None:

        painter = QPainter(self)
        brush = QBrush(QColor("#ff0000"))

        painter.setBrush(brush)
        if self.isVert:
            painter.drawRect(QRect(0, self.value, self.barWidth, self.stepSize))
        else:
            painter.drawRect(QRect(self.value, 0, self.stepSize, self.barWidth))

        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(QColor("#0000ff"), 4)
        painter.setPen(pen)
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
        painter.end()

    def mousePressEvent(self, event) -> None:
        self.clicked = True
        self.clickedOut = not self.barRect().contains(event.position().toPoint())

        if self.clickedOut:
            self.value = (event.position().y() if self.isVert else event.position().x()) - self.stepSize / 2
            self.value = int(max(0, min(self.value, self.displayRange)))
            self.proxy.setValue((self.value / self.displayRange) * self.range)
            
            
        self.lastPos = event.globalPosition()
        event.accept()

    def mouseMoveEvent(self, event) -> None:

        if self.isVert:
            dv = event.globalPosition().y() - self.lastPos.y()
        else:
            dv = event.globalPosition().x() - self.lastPos.x()
        self.value = int(max(0, min(self.value + dv, self.displayRange)))

        self.proxy.setValue((self.value / self.displayRange) * self.range)
        self.lastPos = event.globalPosition()
        event.accept()

    def leaveEvent(self, event) -> None:

        self.clicked = False
        self.lastPos = None
        event.accept()
