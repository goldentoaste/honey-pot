from PyQt5.QtCore import (QRegularExpression, QRegularExpressionMatch,
                          QRegularExpressionMatchIterator)
from PyQt5.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCharFormat,
                         QTextDocument)



def stateContains(state:int, val:int):
    return state % val == 0

def addToState(state:int, val:int):
    if state == 0:
        return val
    return state * val

def removeState(state:int, val:int):
    while (temp := (state // val)) != 0:
        state = temp
    if state == 1:
        return 0
    return state

# prime number based 
emptyState = 0
pythonState = 2
jsState = 3
pythonMLCommentState = 5

if __name__ == '__main__':
    
    state = emptyState
    state = addToState(state, pythonState)
    print(state)
    state = removeState(state, pythonState)
    print(state)



class AbstractParser:
    
    def __init__(self, parser: QSyntaxHighlighter) -> None:
        self.parser = parser
        

    def highlightBlock(self, text:str):
        pass

        
    def currentBlock(self):
        return self.parser.currentBlock()
    
    def setCurrentBlockState(self, state:int):
        self.parser.setCurrentBlockState(state)
    
    def currentBlockState(self):
        return self.parser.currentBlockState()
    
    def previousBlockState(self):
        return self.parser.previousBlockState()
    
    def setFormat(self, start:int, end:int, format: QTextCharFormat):
        self.parser.setFormat(start, end, format)