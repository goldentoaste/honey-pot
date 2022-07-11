import datetime
import os

import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QWidget

from GUI.notePreviewGUI import Ui_NotePreview


class NotePreview(Ui_NotePreview, QWidget):
    def __init__(self, filePath: str) -> None:
        super().__init__()
        self.setupUi(self)

        self.markDown: str = None
        self.filepath = filePath
        
        self.update()

    def update(self):
        """
        grabs the local file and updates the markdown content, and also time stamp
        """
        with open(self.filepath, "r", encoding="utf8") as f:

            self.markDown = f.read()

            self.textBrowser.setMarkdown("\n".join(self.markDown.split(os.linesep, 3)))  # preview the first 3 lines

        # time stuff
        unixTime = os.path.getmtime(self.filepath)
        dt = datetime.datetime.utcfromtimestamp(unixTime)
        if dt.year == datetime.datetime.now().year:
            timeStr = dt.strftime("%b %d, %a")  # Jun 17, Weds etc, hiding year number if is from the current year.
        else:
            timeStr = dt.strftime("%b %d, %Y")
        self.timeLabel.setText(timeStr)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        """
        lauch the full sticky note window.
        """

        a0.accept()
