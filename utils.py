import os
import re
import sys
from PySide6.QtCore import (QRegularExpression, QRegularExpressionMatch,
                          QRegularExpressionMatchIterator)
reflags = QRegularExpression.PatternOption

# FIXME dev location 
cacheLocation = r"D:\PythonProject\stickyMarkdown\testCache"

mdImageRegex = re.compile(r"\!\[[^\[\]]+\]\(([^\(\)]+)\)")  # finds all the image links

mdCodeBlockRegex = re.compile(r"```([\s\S]*?)```")

def getPath(relativePath):
    return os.path.join(os.path.dirname(__file__), relativePath)

if __name__ == "__main__":
    print("testing stuff in utils")

    with open("ref.md", "r", encoding="utf8") as f:
        res = mdImageRegex.findall(f.read())
        for match in res:
            print(type(match))
            print(match)

def lerp(a, b, t):
    return a + t * (b - a)