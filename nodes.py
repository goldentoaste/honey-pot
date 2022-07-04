from PyQt5.QtWidgets import QWidget, QApplication

from GUI.noteGUI import Ui_Note
from PyQt5.QtCore import Qt




class Note(Ui_Note, QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    from qt_material import apply_stylesheet
    apply_stylesheet(app, theme='GUI/colors.xml')
    n = Note()

    n.show()
    sys.exit(app.exec_())
