import sys


from PySide6.QtWidgets import QApplication, QWidget

from GUI.mainGUI import Ui_Form

class Main(Ui_Form, QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    M = Main()
    M.show()

    sys.exit(app.exec())
