
import sys
import os

def getResource( relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)




class A:
    
    def stuff(self):
        print("AAA")


def change(a:A):
    a.stuff = lambda : print("BBB")

    

x = A()
change(x)
x.stuff()