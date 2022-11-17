from PySide6.QtCore import (QRegularExpression, QRegularExpressionMatch,
                          QRegularExpressionMatchIterator)
from PySide6.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCharFormat,
                         QTextDocument)

from codeparser import (AbstractParser, addToState, pythonMLCommentState,
                        removeState, stateContains)

reflags = QRegularExpression.PatternOption


tsKeywords = [
    "class",
    "break",
    "case",
    "module",
    "public",
    "finally",
    "in",
    "package",
    "new",
    "continue",
    "as",
    "if",
    "private",
    "for",
    "super",
    "return",
    "try",
    "do",
    "throw",
    "string",
    "instanceof",
    "enum",
    "while",
    "this",
    "static",
    "interface",
    "yield",
    "catch",
    "switch",
    "else",
    "get",
    "typeof",
    "export",
    "new",
    "function",
    "keyof",
    "import",
    "from",
    "of"
]
'''
keywords (red)
varClass (orange)
types (light blue)
operators (orange)
functions (light green)
singleLineStrings (yellow)
singleLineComment (gray)
typeHint (dark green)
typeDelare (light blue)
classDeclare (dark green)

'''
keywordsRegex = QRegularExpression(r"\b((?:as|break|c(?:a(?:se|tch)|lass|ontinue)|do|e(?:lse|num|xport)|f(?:inally|or|rom|unction)|get|i(?:mport|n(?:(?:stanceof|terface))?|f)|keyof|module|new|of|p(?:ackage|rivate|ublic)|return|s(?:t(?:atic|ring)|uper|witch)|t(?:h(?:is|row)|ry|ypeof)|while|yield))\b")

# to be orange
varClass = ["var", "let", "const", "type", "extends", "implements"]

varClassRegex = QRegularExpression(r"\b(const|extends|implements|let|type|var)\b")


# to be purple / same as numerics
constants = ["true", "false", "null", "undefined", "this", "window", "\.length", ".stack"]
constantsRegex = QRegularExpression(r"\b(false|null|true|undefined|this|window|\.length|\.stack)\b")


# should be blue, none included types aka not builtin/common type names should be green/obj
types = ["void", "string", "boolean", "number", "any"]
typesRegex = QRegularExpression(r"\b(any|boolean|number|string|void|int|console)\b")

# to be orange
operators = ["<", ">", "=", "\+", "\*", "&", "\|", "%", "-", "!", "\?", "~", "^", "\/"]
bar = "|"
operatorsRegex = QRegularExpression(f"{bar.join(operators)}")

functionRegex = QRegularExpression("([a-zA-z_]+[a-zA-z_0-9]*)(?:\()")

stringRegex1 = QRegularExpression(r"\"([^\"])*\"")
stringRegex2 =QRegularExpression(r"\'([^\'])*\'")
multLineStrRegex = QRegularExpression("`") #TODO watch out for escape characters here

commentRegex = QRegularExpression("\/\/[\s\S]*$", reflags.MultilineOption)
multiCommentStartRegex = QRegularExpression("\/\*")
multiCommentEndRegex = QRegularExpression("\*\/")

typeHintRegex = QRegularExpression(r':([\w\s_0-9]+)(?:[,)\n])')
typeDeclareRegex = QRegularExpression(r"(?:type|enum)\s+(\w+)")
classDelareRegex = QRegularExpression(r"(?:class)\s+(\w+)")

numbericsRegex = QRegularExpression("\\b[1-9_.]+\\b")

jsxTagRegex = QRegularExpression("<\/?(\s*\w+)")

class JsParser(AbstractParser):
    def __init__(self, parser: QSyntaxHighlighter) -> None:
        super().__init__(parser)


    def highlightBlock(self, text: str):
        
        keywordsMatches = keywordsRegex.globalMatch(text)
        while keywordsMatches.hasNext():
            match = keywordsMatches.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword)
        
        varClassMatches = varClassRegex.globalMatch(text)
        while varClassMatches.hasNext():
            match = varClassMatches.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.symbol)
        
        typeMatches = typesRegex.globalMatch(text)
        while typeMatches.hasNext():
            match = typeMatches.next()
            self.setFormat(match.capturedStart(), match. capturedLength(),  self.builtin)
        
        operatorsMatches = operatorsRegex.globalMatch(text)
        while operatorsMatches.hasNext():
            match = operatorsMatches.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.symbol )
        
        functionMatchs = functionRegex.globalMatch(text)
        while functionMatchs.hasNext():
            match = functionMatchs.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.function)
        
        stringMatchs = stringRegex1.globalMatch(text)
        while stringMatchs.hasNext():
            match = stringMatchs.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string)
        stringMatchs = stringRegex2.globalMatch(text)
        while stringMatchs.hasNext():
            match = stringMatchs.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string)
        
       
        
        typeHints = typeHintRegex.globalMatch(text)
        while typeHints.hasNext():
            match =typeHints.next()
            self.setFormat(match.capturedStart( 1), match.capturedLength(1), self.obj)
        
        typeDeclareMatch = typeDeclareRegex.match(text)
        if typeDeclareMatch.capturedStart() >= 0:
            self.setFormat(typeDeclareMatch.capturedStart(1), typeDeclareMatch.capturedLength(1), self.obj)
                
        
        constMatches = constantsRegex.globalMatch(text)
        while constMatches.hasNext():
            match = constMatches.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.numeric)
            
        numericMatches = numbericsRegex.globalMatch(text)
        while numericMatches.hasNext():
            match = numericMatches.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.numeric)
        
        
        classMatch = classDelareRegex.match(text)
        self.setFormat(classMatch.capturedStart(1), classMatch.capturedLength(1), self.builtin)
        
        jsxMatches = jsxTagRegex.globalMatch(text)
        while jsxMatches.hasNext():
            match = jsxMatches.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.builtin)
            
        commentMatch = commentRegex.match(text)
        if commentMatch.capturedStart() >= 0:
            self.setFormat(commentMatch.capturedStart(), len(text)-commentMatch.capturedStart(), self.comment)