import threading
from ctypes import byref, windll, wintypes
from typing import Dict

from PySide6.QtCore import (QCoreApplication, QKeyCombination, QObject, Qt,
                            QThread, Signal, Slot)
from PySide6.QtGui import QKeyEvent, QKeySequence

from Hotkeys.baseHotKeyFManager import _BaseHotkeyManager

user32 = windll.user32

WM_HOTKEY = 786
WM_QUIT = 0x0012
PM_REMOVE = 1


class WindowsHotkeyManager(_BaseHotkeyManager):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.workerThread = QThread(self)
        self.worker = Win32KeyWorker()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.start()
        self.worker.startedSig.connect(self.threadStarted)
        self.worker.startSig.emit()
        self.threadId = -1
        self.bindingRefs = {}
        self.bindingId ={}
        self.signalmap = {}
        QCoreApplication.instance().aboutToQuit.connect(self.cleanUp)
        
    @Slot(str, int, int, int)
    def binded(self, name, id, keycode, modcode):
        self.bindingRefs[name] = (keycode, modcode)
        
        self.bindingId [name] = id

    def cleanUp(self):
        # stop worker
        user32.PostThreadMessageA(self.threadId, WM_QUIT, None, None)
        self.workerThread.terminate()

    @Slot(int)
    def threadStarted(self, id):
        self.threadId = id
        

    def bindGlobal(self, name: str, signal: Signal):
        keyStr = self.vals[name]
        if not keyStr:
            return
        print("in bind global", name, signal)
        keyCombo: QKeyCombination = QKeySequence("+".join([*keyStr.split("+")[:-1], "a"]))[0]
        keyMods = keyCombo.keyboardModifiers()
        keyCode = int(keyStr.split("+")[-1])
        modCode = 0x4000
        if Qt.KeyboardModifier.AltModifier & keyMods:
            modCode |= 0x0001
        if Qt.KeyboardModifier.ControlModifier & keyMods:
            modCode |= 0x0002
        if Qt.KeyboardModifier.ShiftModifier & keyMods:
            modCode |= 0x0004
            
            
        
        if name in self.bindingRefs:
            self.worker.unbindSig.emit(self.bindingId[name])
            self.bindingRefs.pop(name)
            self.bindingId.pop(name)
        else:
            self.worker.regNewHK.emit(keyCode, modCode, signal,name)
            self.signalmap[name] = signal
    
    def updateGlobalBinding(self, name: str, keyStr: str):
        self.vals[name]  = keyStr
        self.config.set(self.sections[name], keyStr)
        self.save()
        
        if name not in self.bindingRefs:
            return
        
        self.worker.unbindSig.emit(self.bindingId[name])
        self.bindingId.pop(name)
        self.bindingRefs.pop(name)
        
        self.bindGlobal(name, self.signalmap[name])
        
        


class Win32KeyWorker(QObject):

    regNewHK = Signal(int, int, Signal, str)  # keycode, modcode, callback
    startSig = Signal()
    startedSig = Signal(int)  # returns the thread id
    idRegistered = Signal(int,str)
    unbindSig = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.index = 0
        self.regNewHK.connect(self.regNewHotkey)
        self.bindings: Dict[int, Signal] = {}  # hotkey id mapped to signal to emit
        self.startSig.connect(self.run)
        self.unbindSig.connect(self.unbindKey)
    
    @Slot(int)
    def unbindKey(self, id):
        print('unbind', id)
        user32.UnregisterHotKey(None, id)

    @Slot(int, int, Signal,str)
    def regNewHotkey(self, keycode, modcode, callbackSignal, name):
        self.index += 1
        print('new hk', keycode, modcode, name)
        if user32.RegisterHotKey(None, self.index, modcode, keycode):
            self.bindings[self.index] = callbackSignal
            self.idRegistered.emit(name, self.index, keycode, modcode)

    def run(self) -> None:
        self.startedSig.emit(threading.get_ident())
        msg = wintypes.MSG()
        try:
            while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
                # message ready
                if msg.message == WM_HOTKEY:
                    sig = self.bindings.get(msg.wParam)
                    if sig:
                        sig.emit()
                user32.TranslateMessage(byref(msg))
                user32.DispatchMessageA(byref(msg))
            print("after while")
        finally:
            for id in self.bindings:
                user32.UnregisterHotKey(None, id)
            print("in final")
