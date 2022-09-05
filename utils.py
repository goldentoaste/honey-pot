import sys
import os

#FIXME dev location adas
cacheLocation = r"D:\PythonProject\stickyMarkdown\testCache"

def getResource(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
