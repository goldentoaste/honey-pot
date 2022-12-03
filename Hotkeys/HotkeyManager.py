
from Hotkeys.baseHotKeyFManager import _BaseHotkeyManager
import sys
class HotkeyManager(_BaseHotkeyManager):
    
    '''
    This is just a proxy class that makes a manager specific to a os platform
    '''
    
    def __new__(cls) -> 'HotkeyManager':
        
        platform = sys.platform
        
        if platform =='win32':
            from Hotkeys.windowsHotkey import WindowsHotkeyManager
            return WindowsHotkeyManager()
        elif platform == 'linux':
            raise NotImplementedError()
        elif platform == 'darwin':
            raise NotImplementedError()
        # all other platforms are not supported
        raise NotImplementedError(f"The current platform is not supported: {platform}")