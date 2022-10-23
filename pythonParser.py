from PyQt5.QtCore import (QRegularExpression, QRegularExpressionMatch,
                          QRegularExpressionMatchIterator)
from PyQt5.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCharFormat,
                         QTextDocument)


from codeparser import AbstractParser, stateContains, addToState, removeState
reflags = QRegularExpression.PatternOption


pythonKeywords = [
    "False",
    "None",
    "True",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "lambda",
    "nonlocal",
    "not",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
]

pythonKeywordsRegex = QRegularExpression(f"\\b({'|'.join(pythonKeywords)})\\b")

pythonOperators = ["and", "or", "not", "is", "<", ">", "=", "!", "\+", "-", "\/", "\*", "^", "%", "\/\/", "&", "~"]

pythonOpRegex = QRegularExpression(f"\\b({'|'.join(pythonOperators)})\\b")

pythonBuiltins = [
    "int",
    "float",
    "str",
    "dict",
    "set",
    "complex",
    "list",
    "tuple",
    "range",
    "bytes",
    "bytearray",
    "type",
    "all",
    "any",
    "ascii",
    "bin",
    "bool",
    "callable",
    "classmethod",
    "chr",
    "hex",
    "id",
    "input",
    "iter",
    "super",
    "zip",
    "open",
]

pythonBuiltinRegex = QRegularExpression(f"\\b({'|'.join(pythonBuiltins)})\\b")

class SyntaxColor:
    keyWord = QColor("#ea6962")  # like def, return, raise
    symbol = QColor("#e78a4e")  # +, -, /, ^ etc
    string = QColor("#d8a657")
    function = QColor("#a9b665")
    builtin = QColor("#7daea3")  # builtin or system class
    numeric = QColor("#d3869b")  # or used for specials, for example import statements
    comments = QColor("#928374")

class PythonParser(AbstractParser):
    
    def __init__(self, parser:QSyntaxHighlighter):
        super().__init__(parser)
        self.parser = parser
        
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

        # comments is not supported for markdown, because there is no use case in a sticky note app
        self.comment = QTextCharFormat()  # #928374
        self.comment.setForeground(SyntaxColor.comments)
        self.comment.setFont(codeFont)
        

        self.genericRules = [
            (pythonKeywordsRegex, self.keyword),
            (pythonOpRegex, self.symbol), 
            (pythonBuiltinRegex, self.builtin)
        ]
    
    def highlightBlock(self, text: str):
        
        for rule, format in self.genericRules:
            matches : QRegularExpressionMatchIterator = rule.globalMatch(text)            
            while matches.hasNext():
                match : QRegularExpressionMatch = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
                
                
                
                