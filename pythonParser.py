from PyQt5.QtCore import (QRegularExpression, QRegularExpressionMatch,
                          QRegularExpressionMatchIterator)
from PyQt5.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCharFormat,
                         QTextDocument)

from codeparser import AbstractParser, addToState, removeState, stateContains, pythonMLCommentState

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
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
]

pythonKeywordsRegex = QRegularExpression(
    f"\\b((?:False|None|True|a(?:s(?:(?:sert|ync))?|wait)|break|c(?:lass|ontinue)|de[fl]|e(?:l(?:if|se)|xcept)|f(?:inally|or|rom)|global|i(?:mport|[fn])|lambda|no(?:nlocal|t)|pass|r(?:aise|eturn)|try|w(?:hile|ith)|yield))\\b"
)

pythonOperators = [
    "and",
    "or",
    "not",
    "is",
    "<",
    ">",
    "=",
    "!",
    "\+",
    "-",
    "\/",
    "\*",
    "^",
    "%",
    "\/\/",
    "&",
    "~",
]

pythonOpRegex = QRegularExpression(f"((\sand\s)|(\sor\s)|(\snot\s)|(\sis\s)|<|>|=|!|\+|-|\/|\*|^|%|\/\/|&|~)")

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

pythonBuiltinRegex = QRegularExpression(
    "\\b((?:a(?:ll|ny|scii)|b(?:in|ool|yte(?:array|s))|c(?:allable|hr|lassmethod|omplex)|dict|float|hex|i(?:n(?:put|t)|ter|d)|list|open|range|s(?:et|tr|uper)|t(?:uple|ype)|zip))\\b"
)


pythonNumberics = QRegularExpression("\\b[1-9_.]+\\b")


pythonClassRegex = QRegularExpression(r"class\s+([\w\s]+)(?:\(([\w\s,.]+)\))?\s*:")

class SyntaxColor:
    keyWord = QColor("#ea6962")  # like def, return, raise
    symbol = QColor("#e78a4e")  # +, -, /, ^ etc
    string = QColor("#d8a657")
    function = QColor("#a9b665")
    obj = QColor('#89b482')
    builtin = QColor("#7daea3")  # builtin or system class
    numeric = QColor("#d3869b")  # or used for specials, for example import statements
    comments = QColor("#928374")


class PythonParser(AbstractParser):
    def __init__(self, parser: QSyntaxHighlighter):
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

        selfRegex = QRegularExpression("\\bself\\b")
        self.funcRegex = QRegularExpression("([a-zA-z_]+[a-zA-z_0-9]*)\(")

        self.importregex = QRegularExpression(r"(?:from\s+([\w.]+)\s+)?import\s+\(?([\w.,\s]+)(?:$|\))")
        self.exceptionRegex = QRegularExpression(r"except\s+\(?([\w.,\s]+?)\)?(?:as|:)")
        self.stringPrefixRegex= QRegularExpression(r"(f|u|r|b)(?:'|\")")
        self.string1regex = QRegularExpression(r"\"([^\"])*\"")
        self.string2regex = QRegularExpression(r"\'([^\'])*\'")
        self.commentRegex = QRegularExpression(r"#[^\n]*")
        self.multiline = QRegularExpression(r"\"\"\"|\'\'\'")
        
        self.genericRules = [
            (pythonOpRegex, self.symbol),
            (pythonKeywordsRegex, self.keyword),
            (pythonBuiltinRegex, self.builtin),
            (pythonNumberics, self.numeric),
            (selfRegex, self.numeric),
            (self.string1regex, self.string),
            (self.string2regex, self.string)
        ]

    def highlightBlock(self, text: str):
        importMatchs = self.importregex.globalMatch(text)
        
        while importMatchs.hasNext():
            importMatch = importMatchs.next()
            if importMatch.captured(1) == "":
                self.setFormat(importMatch.capturedStart(2), importMatch.capturedLength(2), self.builtin)
            else:
                self.setFormat(importMatch.capturedStart(1), importMatch.capturedLength(1), self.builtin)
                self.setFormat(importMatch.capturedStart(2), importMatch.capturedLength(2), self.obj)
        
        
        for rule, format in self.genericRules:
            matches: QRegularExpressionMatchIterator = rule.globalMatch(text)
            while matches.hasNext():
                match: QRegularExpressionMatch = matches.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        funcMatchs: QRegularExpressionMatchIterator = self.funcRegex.globalMatch(text)
        while funcMatchs.hasNext():
            match: QRegularExpressionMatch = funcMatchs.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.function)

        
        exceptMatch = self.exceptionRegex.match(text)
        self.setFormat(exceptMatch.capturedStart(1), exceptMatch.capturedLength(1), self.obj)

        prefixMatch = self.stringPrefixRegex.match(text)
        self.setFormat(prefixMatch.capturedStart(1), prefixMatch.capturedLength(1), self.builtin) 
    
        classMatch = pythonClassRegex.match(text)
        for i in range(1, len(classMatch.capturedTexts()), 1):
            self.setFormat(classMatch.capturedStart(i), classMatch.capturedLength(i), self.obj)
    
    
        # comment overrides all
        commentMatch = self.commentRegex.match(text)
        self.setFormat(commentMatch.capturedStart(), commentMatch.capturedLength(), self.comment) 
        
        # multiline strings :skull:
        if stateContains(self.previousBlockState(), pythonMLCommentState):
            endMatch = self.multiline.match(text)
            if endMatch.capturedStart() < 0:
                self.setCurrentBlockState(addToState(self.currentBlockState(), pythonMLCommentState))
                self.setFormat(0, len(text), self.string)
            else:
                self.setFormat(0, endMatch.capturedEnd(), self.string)
        else:
            matches = self.multiline.globalMatch(text)
            matchlist = []
            while matches.hasNext():
                matchlist.append(matches.next())
            
            if len(matchlist) == 1:
                match : QRegularExpressionMatch= matchlist[0]
                self.setFormat(match.capturedStart(), len(text) - match.capturedStart(), self.string)
                self.setCurrentBlockState(addToState(self.currentBlockState(), pythonMLCommentState))
            elif len(matchlist) > 1: # igoring multiple multiline strings occuring in the same line
                start = matchlist[0]
                end:QRegularExpressionMatch = matchlist[1]
                self.setFormat(start.capturedStart(), end.capturedEnd() - start.capturedStart(), self.string)
            