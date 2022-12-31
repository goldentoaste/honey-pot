from PySide6.QtCore import Slot
from PySide6.QtGui import QColor, QFont, QTextCharFormat

from Configs.appConfig import getAppConfig


def textFormat(color: QColor, font: QFont, size: int = 10, italic=False, bold=False):
    s = QTextCharFormat()
    s.setForeground(color)
    s.setFont(font)
    s.setFontPointSize(size)

    if italic:
        s.setFontItalic(italic)

    if bold:
        s.setFontWeight(QFont.Weight.Bold)
    return s


class TextStyles:
    def __init__(self):

        getAppConfig().configChanged.connect(self.makeStyles)
        self.makeStyles()

    @Slot()
    def makeStyles(self):
        config = getAppConfig()

        self.keywordColor = QColor(config.sKeyWordColor)
        self.symbolColor = QColor(config.sSymbolColor)
        self.stringColor = QColor(config.sStringColor)
        self.functionColor = QColor(config.sFunctionColor)
        self.builtinColor = QColor(config.sBuiltinColor)
        self.numericsColor = QColor(config.sNumericColor)
        self.commentColor = QColor(config.sCommentColor)
        self.codeTextColor = QColor(config.sTextColor)
        self.codeBlockColor = QColor(config.sBackGroundColor)

        self.codeFont = QFont(config.sCodeFont)
        self.textFont = QFont(config.sTextFont)

        self.editorFontSize = config.iEditorFontSize
        self.previewFontSize = config.iPreviewFontSize

        self.editorBackgroundColor = config.sEditorBackground
        self.previewBackgroundColor = config.sPreviewBackground

        self.keywordFormat = textFormat(self.keywordColor, self.codeFont,self.editorFontSize)
        self.symbolFormat = textFormat(self.symbolColor, self.codeFont,self.editorFontSize)
        self.stringFormat = textFormat(self.stringColor, self.codeFont,self.editorFontSize)
        self.functionFormat = textFormat(self.functionColor, self.codeFont,self.editorFontSize)
        self.builtinFormat = textFormat(self.builtinColor, self.codeFont,self.editorFontSize)
        self.numericsFormat = textFormat(self.numericsColor, self.codeFont,self.editorFontSize)
        self.commentFormat = textFormat(self.commentColor, self.codeFont,self.editorFontSize)

        self.previewTextFormat = textFormat(self.)