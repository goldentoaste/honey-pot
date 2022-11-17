import glob
import os


for item in glob.glob(os.getcwd() + r"\GUI\*.ui"):
    os.system(f"pyside6-uic {item}  -o {item[:-3] + 'GUI.py'}")