import glob
import os


for item in glob.glob(os.getcwd() + r"\GUI\*.ui"):
    os.system(f"pyuic5 {item} -x -o {item[:-3] + 'GUI.py'}")