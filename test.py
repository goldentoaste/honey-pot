
# from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QToolButton
# import sys
import time
import random
# if __name__ == '__main__':
    
#     t0 = time.time()
#     for i in range(100000):
#         x = [random.random() for _ in range(1000)]
#         x.sort()
#     print(time.time()- t0)
#     input("press enter to stop")
    
if __name__ == '__main__':
    
    t0 = time.time()
    x = 0
    for i in range(100000000):
        x += random.random()
    print(time.time()- t0)
    input("press enter to stop")
    
    
    # a = QApplication(sys.argv)
    # w = QWidget()
    # b = QToolButton(w)
    # b.setStyleSheet(
    #     '''
    #     QToolButton {
    #         background-color: #ff0000
    #     }
    #     '''
    # )
    # w.show()
    # a.exec()