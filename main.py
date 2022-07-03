
import sys,os

from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication, QImage, QTextBlock, QTextCursor, QTextImageFormat
from PyQt5.QtQml import QQmlApplicationEngine
from qt_material import apply_stylesheet
from PyQt5.QtCore import Qt

from GUI.mainGUI import Ui_MainWindow
from GUI.notePreviewGUI import Ui_NotePreview

class Main(Ui_MainWindow, QMainWindow):
    
    
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        
class NoteTest(Ui_NotePreview, QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        
        with open("test.md", "r", encoding='utf8') as f:
            self.textBrowser.setMarkdown(f.read(),)
            
        doc = self.textBrowser.document()
        cursor = self.textBrowser.textCursor()
        block = doc.begin()
        
        while block.isValid():
            bit : QTextBlock.iterator = block.begin()
            
            while not bit.atEnd():
                frag = bit.fragment()
                textFormat = frag.charFormat()

                print(textFormat, textFormat.isImageFormat())
                
                if textFormat.isImageFormat():
                    image = textFormat.toImageFormat()
                    print(f"Image! {image.name()}, {frag.position() , frag.length()}")
                    
                    
                    cursor.setPosition(frag.position(), QTextCursor.MoveAnchor)
                    cursor.setPosition(frag.position() + frag.length(), QTextCursor.KeepAnchor)
                    cursor.removeSelectedText()
                    cursor.insertImage(QImage(r"D:\PythonProject\stickyMarkdown\devineInspiration.png"),"wowies!" )
                    
                    
                    # image.setName(r"D:\PythonProject\stickyMarkdown\devineInspiration.png")
                    
                bit +=1
            print("block finished, going next block")
            block = block.next()
        block = doc.begin()
        

        with open("out.html", "w", encoding="utf-8") as out:
            out.write(doc.toHtml())
            
if __name__ == "__main__":
    
    
    app = QApplication(sys.argv)
    

    apply_stylesheet(app, theme='GUI/colors.xml')
    # main = Main()
    # main.show()
    
    t = NoteTest()
    t.show()
    sys.exit(app.exec_())