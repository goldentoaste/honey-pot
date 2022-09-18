

from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QTextDocument, QFont
from PyQt5.QtCore import QRegularExpression, QRegularExpressionMatchIterator, QRegularExpressionMatch
from typing import NamedTuple, List
reflags = QRegularExpression.PatternOption
class SyntaxColor:
    keyWord = QColor("#ea6962") # like def, return, raise
    symbol = QColor("#e78a4e") # +, -, /, ^ etc
    string= QColor("#d8a657")
    function = QColor("#a9b665")
    builtin = QColor("#7daea3") # builtin or system class
    numeric = QColor("#d3869b") # or used for specials, for example import statements
    comments = QColor("#928374") 
    # text = QColor("#d4be98") # generic text


class HighlightRule(NamedTuple):
    regex: QRegularExpression
    format: QTextCharFormat

class Highlighter(QSyntaxHighlighter):
    
    
    def __init__(self, parent: QTextDocument, highlightMakrdown = True):
        
        super().__init__(parent)
        
        codeFont = QFont("Cascadia Code", 9)
        
        self.keyword = QTextCharFormat()# #ea6962
        self.keyword.setForeground(SyntaxColor.keyWord)
        self.keyword.setFont(codeFont)
        
        self.symbol = QTextCharFormat() # #e78a4e
        self.symbol.setForeground(SyntaxColor.symbol)
        self.symbol.setFont(codeFont)
        
        self.string = QTextCharFormat() # #d8a657
        self.string.setForeground(SyntaxColor.string)
        self.string.setFont(codeFont)
        
        self.function = QTextCharFormat() # #a9b665
        self.function.setForeground(SyntaxColor.function)
        self.function.setFont(codeFont)
         
        self.builtin = QTextCharFormat() # #7daea3
        self.builtin.setForeground(SyntaxColor.builtin)
        self.builtin.setFont(codeFont)
        
        self.numeric = QTextCharFormat() # #d3869b
        self.numeric.setForeground(SyntaxColor.numeric)
        self.numeric.setFont(codeFont)
        
        # comments is not supported for markdown, because there is no use case in a sticky note app
        self.comment = QTextCharFormat() # #928374
        self.comment.setForeground(SyntaxColor.comments)
        self.comment.setFont(codeFont)
        
        self.bold = QTextCharFormat()
        self.bold.setFont(codeFont)
        self.bold.setFontWeight(75) # 75 is bold
        

        self.italic = QTextCharFormat()
        self.italic.setFont(codeFont)
        self.italic.setFontItalic(True) 
        
        
        self.boldItalic = QTextCharFormat()
        self.boldItalic.setFont(codeFont)
        self.boldItalic.setFontWeight(75)
        self.boldItalic.setFontItalic(True)
        
        
        


        mdGenericPatterns = ( 
            # all the 1 capture group stuff go here
            (r"^[\t\ ]*#[\t\ ]+([^\n]+)", self.keyword), # highlight the word, make tag comment
            (r"^[\t\ ]*##[\t\ ]+([^\n]+)", self.symbol),
            (r"^[\t\ ]*###[\t\ ]+([^\n]+)", self.string),
            (r"^[\t\ ]*####[\t\ ]+([^\n]+)", self.function),
            (r"^[\t\ ]*#####[\t\ ]+([^\n]+)", self.builtin),
            (r"^[\t\ ]*######[\t\ ]+([^\n]+)", self.numeric), # title ends here
            
            (r"^[\t\ ]*([-+*])[\t\ ]", self.keyword), # bullet point
            (r"[*_]\b([\s\S]*?)\b[*_]", self.italic), # *italic*
            (r"[*_]{2}\b([\s\S]*?)\b[*_]{2}", self.bold), # **BOLD**
            (r"[*_]{3}\b([\s\S]*?)\b[*_]{3}", self.boldItalic), # ***BOLD_ITALIC***
            (r"^([-*]{3,})$", self.symbol)
        )
        
        
    
        
        
        self.genericRules : List[HighlightRule] = [
            (
                QRegularExpression(pattern, reflags.MultilineOption),
                format
            )
            for pattern, format in mdGenericPatterns
        ]
        
        
    def highlightBlock(self, text: str) -> None:
        
        for rule, format in self.genericRules:
            matches : QRegularExpressionMatchIterator= rule.globalMatch(text)
            
            while matches.hasNext():
                match : QRegularExpressionMatch = matches.next()
                print("match", match.capturedTexts())
                self.setFormat(match.capturedStart(),  match.capturedLength(), format)
        
    
    def testing(self):
        print("in testing")
        self.keywordFormat = QTextCharFormat()
        self.keywordFormat.setForeground(SyntaxColor.keyWord)
