import sys
import os
import re

from time import time
#FIXME dev location adas
cacheLocation = r"D:\PythonProject\stickyMarkdown\testCache"

mdImageRegex = re.compile(r"\!\[[^\[\]]+\]\(([^\(\)]+)\)") # finds all the image links

mdCodeBlockRegex = re.compile(r"```([\s\S]*?)```")

def getResource(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    print("testing stuff in utils")
    
    with open('ref.md', 'r', encoding='utf8') as f:
        res = mdImageRegex.findall(f.read())
        for match in res:
            print(type(match))
            print(match)