from PyQt5.QtCore import (QRegularExpression, QRegularExpressionMatch,
                          QRegularExpressionMatchIterator)
from PyQt5.QtGui import (QColor, QFont, QSyntaxHighlighter, QTextCharFormat,
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
]

keywordsRegex = QRegularExpression(r"\b((?:as|break|c(?:a(?:se|tch)|lass|ontinue)|do|e(?:lse|num|xport)|f(?:inally|or|unction)|get|i(?:mport|n(?:(?:stanceof|terface))?|f)|keyof|module|new|p(?:ackage|rivate|ublic)|return|s(?:t(?:atic|ring)|uper|witch)|t(?:h(?:is|row)|ry|ypeof)|while|yield))\b")

# to be orange
varClass = ["var", "let", "const", "type", "extends", "implements"]

varClassRegex = QRegularExpression(r"\b(const|extends|implements|let|type|var)\b")


# to be purple / same as numerics
constants = ["true", "false", "null", "undefined", "this", "window", "\.length", ".stack"]
constantsRegex = QRegularExpression(r"\b(false|null|true|undefined|this|window|\.length|\.stack)\b")


# should be blue, none included types aka not builtin/common type names should be green/obj
types = ["void", "string", "boolean", "number", "any"]
typesRegex = QRegularExpression(r"\b(any|boolean|number|string|void)\b")

# to be orange
operators = ["<", ">", "=", "\+", "\*", "&", "\|", "%", "-", "!", "\?", "~", "^", "\/"]
slashBar = "\|"
operatorsRegex = QRegularExpression(f"\\b{slashBar.join(operators)}\\b")

functionRegex = QRegularExpression("([a-zA-z_]+[a-zA-z_0-9]*)\(")

stringRegex1 = QRegularExpression(r"\"([^\"])*\"")
stringRegex2 =QRegularExpression(r"\'([^\'])*\'")
multLineStrRegex = QRegularExpression("`") #TODO watch out for escape characters here

commentRegex = QRegularExpression("\/\/[\s\S]*$", reflags.MultilineOption)
multiCommentStartRegex = QRegularExpression("\/\*")
multiCommentEndRegex = QRegularExpression("\*\/")


class JsParser(AbstractParser):
    def __init__(self, parser: QSyntaxHighlighter) -> None:
        super().__init__(parser)
