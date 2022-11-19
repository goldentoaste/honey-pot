
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout

import sys
if __name__ == '__main__':
    
    a = QApplication(sys.argv)
    
    w = QWidget()
    l = QLabel("testing!!")
    
    layout = QVBoxLayout()
    layout.addWidget(l)
    w.setLayout(layout)
    
    w.show()
    sys.exit(a.exec())
