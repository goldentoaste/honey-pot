import os
import re
import sys

# FIXME dev location adas
cacheLocation = r"D:\PythonProject\stickyMarkdown\testCache"

mdImageRegex = re.compile(r"\!\[[^\[\]]+\]\(([^\(\)]+)\)")  # finds all the image links

mdCodeBlockRegex = re.compile(r"```([\s\S]*?)```")

pythonKeywods = [
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

pythonOperators = [
    "and", "or", "not", "is", "<",">","=", "!","+","-","/","*","^", "%", "//", "&","~"
]

pythonTypes = [
    "int","float","str","dict", "set", "complex", "list","tuple","range", "bytes", "bytearray"
]

def getResource(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    print("testing stuff in utils")

    with open("ref.md", "r", encoding="utf8") as f:
        res = mdImageRegex.findall(f.read())
        for match in res:
            print(type(match))
            print(match)
