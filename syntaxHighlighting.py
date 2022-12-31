from enum import Enum, IntFlag, auto
from re import L
from typing import List, NamedTuple, Tuple

from PySide6.QtCore import (QRegularExpression, QRegularExpressionMatch,
                            QRegularExpressionMatchIterator)
from PySide6.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCharFormat,
                           QTextDocument)

from codeparser import (addToState, emptyState, jsState, pythonState,
                        removeState, stateContains)
from jsParser import JsParser
from pythonParser import PythonParser

reflags = QRegularExpression.PatternOption


class Languages(Enum):
    python = auto()
    javascript = auto()
    text = auto()
    none = auto()


class SyntaxColor:
    keyWord = QColor("#ea6962")  # like def, return, raise
    symbol = QColor("#e78a4e")  # +, -, /, ^ etc
    string = QColor("#d8a657")
    function = QColor("#a9b665")
    builtin = QColor("#7daea3")  # builtin or system class
    numeric = QColor("#d3869b")  # or used for specials, for example import statements
    comments = QColor("#928374")
    text = QColor("#d4be98") # generic text


class PreviewHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument):
        super().__init__(parent)
        self.blockLangs: List[Languages] = []
        self.blockLengths: List[Tuple[int, int]] = []  # Tuple[Start, EndIndex]

        self.pythonStart = QRegularExpression("^\\x{200b}\\x{200b}(?!\\x{200b})", reflags.MultilineOption)
        self.jsStart = QRegularExpression("^\\x{200b}\\x{200b}\\x{200b}", reflags.MultilineOption)
        self.codeEndPattern = QRegularExpression("\\x{200c}$", reflags.MultilineOption)

        self.startIndex = 0
        self.matchLength = 0

        self.offset = 0

        self.pythonParser = PythonParser(self)
        self.jsParser = JsParser(self)

    def reset(self):

        self.blockLangs.clear()
        self.blockLengths.clear()

        self.startIndex = 0
        self.matchLength = 0
        self.offset = 0

    def updateCodeBlock(self, newBlocks):
        self.blockLangs = newBlocks
        self.matchLength = 0

    def highlightBlock(self, text: str) -> None:
        self.checkPython(text)
        self.checkJS(text)

    def checkJS(self, text: str):
        if stateContains(self.previousBlockState(), jsState):
            endMatch = self.codeEndPattern.match(text)
            self.jsParser.highlightBlock(text)
            if endMatch.capturedStart() < 0:
                self.setCurrentBlockState(addToState(self.currentBlockState(), jsState))
        else:
            startMatch = self.jsStart.match(text)
            endMatch = self.codeEndPattern.match(text)
            if startMatch.capturedStart() >= 0:
                self.jsParser.highlightBlock(text)
                if endMatch.capturedStart() < 0:
                    self.setCurrentBlockState(addToState(self.currentBlockState(), jsState))

    def checkPython(self, text: str):
        if stateContains(self.previousBlockState(), pythonState):
            endMatch = self.codeEndPattern.match(text)
            self.pythonParser.highlightBlock(text)
            if endMatch.capturedStart() < 0:
                self.setCurrentBlockState(addToState(self.currentBlockState(), pythonState))
        else:
            startMatch = self.pythonStart.match(text)
            endMatch = self.codeEndPattern.match(text)
            if startMatch.capturedStart() >= 0:
                self.pythonParser.highlightBlock(text)
                if endMatch.capturedStart() < 0:
                    self.setCurrentBlockState(addToState(self.currentBlockState(), pythonState))


NoneState = 0
CodeBLockState = 2  # check state using prime numbers and modulo


class EditorHighlighter(QSyntaxHighlighter):
    def __init__(self, parent: QTextDocument, highlightMakrdown=True):

        super().__init__(parent)

        codeFont = QFont("Cascadia Code", 9)

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

        self.builtin = QTextCharFormat()  # #7daea3
        self.builtin.setForeground(SyntaxColor.builtin)
        self.builtin.setFont(codeFont)

        self.numeric = QTextCharFormat()  # #d3869b
        self.numeric.setForeground(SyntaxColor.numeric)
        self.numeric.setFont(codeFont)
        
        self.errorColor = QTextCharFormat()
        self.errorColor.setBackground(QColor(234, 105, 98, 100))
        self.indentColors = [
            QTextCharFormat(),
            QTextCharFormat(),
            QTextCharFormat(),
            QTextCharFormat(),
        ]
        
        for f,c in zip(self.indentColors,(  QColor(216, 166, 87, 100),
            QColor(169, 182, 101, 100),
            QColor(211, 134, 155,100),
            QColor(125, 174, 163,100))):
            f.setBackground(c)

        # comments is not supported for markdown, because there is no use case in a sticky note app
        self.comment = QTextCharFormat()  # #928374
        self.comment.setForeground(SyntaxColor.comments)
        self.comment.setFont(codeFont)

        self.bold = QTextCharFormat()
        self.bold.setFont(codeFont)
        self.bold.setFontWeight(QFont.Weight.Bold)  # 75 is bold

        self.italic = QTextCharFormat()
        self.italic.setFont(codeFont)
        self.italic.setFontItalic(True)

        self.boldItalic = QTextCharFormat()
        self.boldItalic.setFont(codeFont)
        self.boldItalic.setFontWeight(QFont.Weight.Bold)
        self.boldItalic.setFontItalic(True)

        mdGenericPatterns = (
            # all the 1 capture group stuff go here
            (r"^[\t\ ]*#[\t\ ]+([^\n]+)", self.keyword),  # highlight the word, make tag comment
            (r"^[\t\ ]*##[\t\ ]+([^\n]+)", self.symbol),
            (r"^[\t\ ]*###[\t\ ]+([^\n]+)", self.string),
            (r"^[\t\ ]*####[\t\ ]+([^\n]+)", self.function),
            (r"^[\t\ ]*#####[\t\ ]+([^\n]+)", self.builtin),
            (r"^[\t\ ]*######[\t\ ]+([^\n]+)", self.numeric),  # title ends here
            (r"^[\t\ ]*([-+*])[\t\ ]", self.keyword),  # bullet point
            (r"(?<!\*)[*_](?!\s)([^*_]+?)(?<!\s)[*_](?!\*)", self.italic),  # *italic*
            (r"(?<!\*)[*_]{2}(?!\s)([^*_]+?)(?<!\s)[*_]{2}(?!\*)", self.bold),  # **BOLD**
            (r"(?<!\*)[*_]{3}(?!\s)([^*_]+?)(?<!\s)[*_]{3}(?!\*)", self.boldItalic),  # ***BOLD_ITALIC***
            (r"^([-*]{3,})$", self.symbol),
            (r"(?:^|\s)(`[^`]+?`)(?:\s|$)", self.keyword),
        )

        self.linkPattern = QRegularExpression(r"\[([\s\S]*?)\]\(([\s\S]+?)\)", reflags.MultilineOption)

        self.genericRules: List[Tuple[QRegularExpression, QTextCharFormat]] = [
            (QRegularExpression(pattern, reflags.MultilineOption), format) for pattern, format in mdGenericPatterns
        ]

        self.codeBlockStartPattern = QRegularExpression(r"^```", reflags.MultilineOption)
        self.codeblockLangPattern = QRegularExpression(r"txt|text|python|py|js|javascript|ts|typescipt")
        self.codeBlockEndPattern = QRegularExpression(r"```\s*$", reflags.MultilineOption)
        self.indentRegex = QRegularExpression(r"^\s+", reflags.MultilineOption)
        self.newLineRegex = QRegularExpression(r"  $", reflags.MultilineOption)
        self.codeStartIndex = 0
        
        

    def highlightBlock(self, text: str) -> None:
        for rule, format in self.genericRules:
            matches: QRegularExpressionMatchIterator = rule.globalMatch(text)
            while matches.hasNext():
                match: QRegularExpressionMatch = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        # format links
        linkMatches = self.linkPattern.globalMatch(text)
        while linkMatches.hasNext():
            match: QRegularExpressionMatch = linkMatches.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.numeric)
            self.setFormat(match.capturedStart(2), match.capturedLength(2), self.function)

        # codeblock formatting
        self.setCurrentBlockState(1)
        startIndex = 0
        matchLength = 0
        startMatch = None
        # if prevState is not comment
        if self.previousBlockState() % CodeBLockState:
            startMatch = self.codeBlockStartPattern.match(text)
            startIndex = startMatch.capturedStart()

        if startIndex >= 0:
            if startMatch is not None:
                offset = startMatch.capturedLength()
            else:
                offset = 0
            endMatch = self.codeBlockEndPattern.match(text, offset)
            endindex = endMatch.capturedStart()

            if endindex == -1:
                matchLength = len(text) - startIndex
                self.setCurrentBlockState(self.currentBlockState() * CodeBLockState)
            else:
                matchLength = endindex - startIndex + endMatch.capturedLength()
            self.setFormat(startIndex, matchLength, self.keyword)

            if self.previousBlockState() % CodeBLockState:
                langMatch = self.codeblockLangPattern.match(text)
                if langMatch.capturedStart() != -1:
                    self.setFormat(langMatch.capturedStart(), langMatch.capturedLength(), self.builtin)

        # highlighting indent
        
        indentMatch = self.indentRegex.match(text)

        spaceCounter = 0
        colorIndex = -1
        for i in range(indentMatch.capturedStart(), indentMatch.capturedEnd()):
            
            if text[i] == " ":
                spaceCounter += 1
            elif text[i] == "\t":
                if spaceCounter > 0:
                    print(spaceCounter, i - spaceCounter-1)
                    self.setFormat(i - spaceCounter, spaceCounter, self.errorColor)  
                spaceCounter = 999
                
                
            if spaceCounter == 4:
                colorIndex += 1
                colorIndex %= len(self.indentColors)
                self.setFormat(i - spaceCounter + 1, spaceCounter, self.indentColors[colorIndex])
                spaceCounter = 0
                
            if spaceCounter == 999: # handling tab chars
                colorIndex += 1
                colorIndex %= len(self.indentColors)
                self.setFormat(i , 1, self.indentColors[colorIndex])
                spaceCounter = 0
        
        if spaceCounter >0:
            self.setFormat(indentMatch.capturedEnd() - spaceCounter, spaceCounter, self.errorColor)
            
        newLineMatch =  self.newLineRegex.match(text)
        if newLineMatch.capturedStart() >0:
            self.setFormat(newLineMatch.capturedStart(), newLineMatch.capturedLength(), self.errorColor)