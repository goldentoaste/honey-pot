import glob
import os


os.system(f"pyside6-rcc {os.getcwd()}\GUI\stickyResource.qrc -o {os.getcwd()}\GUI\stickyResource_rc.py")
for item in glob.glob(os.getcwd() + r"\GUI\*.ui"):
    os.system(f"pyside6-uic {item} --from-imports GUI -o {item[:-3] + 'GUI.py'}")