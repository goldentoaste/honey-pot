from ctypes import byref, windll, wintypes
from time import sleep as seep
from typing import Dict

from PySide6.QtCore import QKeyCombination, Qt, QThread, Signal, Slot, QObject
from PySide6.QtGui import QKeyEvent, QKeySequence

from Hotkeys.baseHotKeyFManager import _BaseHotkeyManager
import threading
user32 = windll.user32

WM_HOTKEY = 786
PM_REMOVE = 1




class WindowsHotkeyManager(_BaseHotkeyManager):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.workerThread = QThread(self)
        self.worker = Win32KeyWorker()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()
        self.worker.startSig.emit()
 

    def bindGlobal(self, name: str, signal: Signal):
        keyStr = self.vals[name]
        if not keyStr:
            return

        keyCombo: QKeyCombination = QKeySequence("+".join([*keyStr.split("+")[:-1], 'a']))[0]
        keyMods = keyCombo.keyboardModifiers()
        keyCode = int(keyStr.split("+")[-1])
        modCode = 0x4000
        if Qt.KeyboardModifier.AltModifier & keyMods:
            modCode |= 0x0001
        if Qt.KeyboardModifier.ControlModifier & keyMods:
            modCode |= 0x0002
        if Qt.KeyboardModifier.ShiftModifier & keyMods:
            modCode |= 0x0004

        self.worker.regNewHK.emit(keyCode, modCode, signal)

class Win32KeyWorker(QObject):

    regNewHK = Signal(int, int, Signal)  # keycode, modcode, callback
    startSig = Signal()

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.index = 0
        self.regNewHK.connect(self.regNewHotkey)
        self.bindings: Dict[int, Signal] = {}  # hotkey id mapped to signal to emit
        self.startSig.connect(self.run)
        
    @Slot(int, int, Signal)
    def regNewHotkey(self, keycode, modcode, callbackSignal):
        self.index += 1
        
        print(keycode, modcode)
        if user32.RegisterHotKey(None, self.index, modcode, keycode):
            print("binding yes")
            self.bindings[self.index] = callbackSignal
        else:
            print("binding NOOO")
            

    # def run(self) -> None:
    #     msg = wintypes.MSG()
    #     try:
    #         while True:
    #             if user32.PeekMessageA(byref(msg), None, 0, 0, PM_REMOVE):
    #                 print("ready",msg.message)
    #                 # message ready
    #                 if msg.message == WM_HOTKEY:
    #                     sig = self.bindings.get(msg.wParam)
    #                     if sig:
    #                         sig.emit()
    #                 user32.TranslateMessage(byref(msg))
    #                 user32.DispatchMessageA(byref(msg))
    #             seep(0.1)
    #     finally:
    #         for id in self.bindings:
    #             user32.UnregisterHotKey(None, id)
    
    def run(self) -> None:
        msg = wintypes.MSG()
        try:
            while True:
                print(msg)
                if user32.GetMessageA(byref(msg), None, 0, 0)!=0:
                    # message ready
                    if msg.message == WM_HOTKEY:
                        sig = self.bindings.get(msg.wParam)
                        if sig:
                            sig.emit()
                else:
                    break
                user32.TranslateMessage(byref(msg))
                user32.DispatchMessageA(byref(msg))

        finally:
            for id in self.bindings:
                user32.UnregisterHotKey(None, id)

