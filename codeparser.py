from PySide6.QtCore import (QRegularExpression, QRegularExpressionMatch,
                            QRegularExpressionMatchIterator)
from PySide6.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCharFormat,
                           QTextDocument)


def stateContains(state: int, val: int):
    return state % val == 0


def addToState(state: int, val: int):
    if state == 0:
        return val
    return state * val


def removeState(state: int, val: int):
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

if __name__ == "__main__":

    state = emptyState
    state = addToState(state, pythonState)
    print(state)
    state = removeState(state, pythonState)
    print(state)


class SyntaxColor:
    keyWord = QColor("#ea6962")  # like def, return, raise
    symbol = QColor("#e78a4e")  # +, -, /, ^ etc
    string = QColor("#d8a657")
    function = QColor("#a9b665")
    obj = QColor("#89b482")
    builtin = QColor("#7daea3")  # builtin or system class
    numeric = QColor("#d3869b")  # or used for specials, for example import statements
    comments = QColor("#928374")


class AbstractParser:
    def __init__(self, parser: QSyntaxHighlighter) -> None:
        self.parser = parser

        self.currentBlock = self.parser.currentBlock
        self.setCurrentBlockState = self.parser.setCurrentBlockState
        self.currentBlockState = self.parser.currentBlockState
        self.previousBlockState = self.parser.previousBlockState
        self.setFormat = self.parser.setFormat
        # self.setFormat = lambda *args:()

        codeFont = QFont("Cascadia Code", 10)

        self.keyword = QTextCharFormat()  # #ea6962
        self.keyword.setForeground(SyntaxColor.keyWord)
        self.keyword.setFont(codeFont)

        self.symbol = QTextCharFormat()  # #e78a4e
        self.symbol.setForeground(SyntaxColor.symbol)
        self.symbol.setFont(codeFont)

        self.string = QTextCharFormat()  # #d8a657
        self.string.setForeground(SyntaxColor.string)
        self.string.setFont(codeFont)

        self.function = QTextCharFormat()  # #a9b665
        self.function.setForeground(SyntaxColor.function)
        self.function.setFont(codeFont)

        self.obj = QTextCharFormat()  # #89b482
        self.obj.setForeground(SyntaxColor.obj)
        self.obj.setFont(codeFont)

        self.builtin = QTextCharFormat()  # #7daea3
        self.builtin.setForeground(SyntaxColor.builtin)
        self.builtin.setFont(codeFont)

        self.numeric = QTextCharFormat()  # #d3869b
        self.numeric.setForeground(SyntaxColor.numeric)
        self.numeric.setFont(codeFont)

        # comments is not supported for markdown, because there is no use case in a sticky note app
        self.comment = QTextCharFormat()  # #928374
        self.comment.setForeground(SyntaxColor.comments)
        self.comment.setFont(codeFont)

    def highlightBlock(self, text: str):

        pass

    # def currentBlock(self):
    #     return self.parser.currentBlock()

    # def setCurrentBlockState(self, state:int):
    #     self.parser.setCurrentBlockState(state)

    # def currentBlockState(self):
    #     return self.parser.currentBlockState()

    # def previousBlockState(self):
    #     return self.parser.previousBlockState()

    # def setFormat(self, start:int, end:int, format: QTextCharFormat):
    #     self.parser.setFormat(start, end, format)
