
# Sticky honey pot todos 🍯

## Current task:
* implement some main menu features:
    + ~~make general layouting~~
    + make menu page for mardown editing and key bindings
    + skip notes management and list for now
* separate global config by sections
    * hotkey section (which is ready)
    * general section (like lauch on start up for example)
    * style section
        * indicated by Style.section name
        * have a drop down to select style set.

* ConfigManger should generate its gui that modifies itself, base on current schema.    
* [x] Hotkey Manager should generate a gui to edit all the key bindings.

* implement copying images in preview 
* fix/hide QSpliiter when Editor is hidden and exiting editing mode.

* add convience hotkeys
    - should all be rebinable
    - (done)ctrl 8(*) for wrapping current selection in star once (or currrent line is no selection) (strip space)
    - (done)ctrl I to make selection italic (just wrap * once)
    - (done)ctrl B to make selection Bold (wrapping * twice)
    - (done)ctrl `(~) to cross out current selection (wrap ~ twice)
    - (done)ctrl 3(#) to append 1 # at the beginning of current line
    
    - ctrl space to insert `&nbsp;` once as non removing space (although it seems like Qt preserves space. :/)
                    - maybe a key to make inserting image link or text link quicker, not decided yet.

    * (current):
    - Ctrl + Tab indents current line by 1, or until the next 4 space increment
    - Shift + Tab de-indent the current line
    - improvements to make:
        + if an hotkey operation effects the whole line/insert at beginning, it should skip any valid markdown symbols, then start applying their effects there.



* add emoji support (way later)
    - should respect escaped `\:`
    - cast common emoji like `:/ :) :( ;-;` etc to a unicode emoji, (should be an setting boolean to disable)
    - should show a auto complete widget when typing starting with `:`
        + `:br`->
        + `:bread`
        + `bricks`
        + `brain` etc

--include-data-file=Hotkeys\windowsHotkey.py=Hotkeys\windowsHotkey.py
```
build
nuitka notes.py  --enable-plugin=pyside6 --onefile --standalone  --include-data-dir=GUI=GUI  --windows-disable-console  --show-memory --show-progress --plugin-enable=upx --include-plugin-files=Hotkeys\windowsHotkey.py
```




* ~~write javascript parser~~ (done, kinda)
    - try to support type script, since js is a strict subset
* ~~fix bugs regarding window edge drag to scale~~


* ~~write a new config manager (do this next, then go back to scrollbars visuals)~~ (done)
    - use a json like/python dict like interface to define schema
    - should handle multiple variable types as before
    - self modifying code:
        - generate type hinting file in a meta class to type hint for a default schema layout

* ~~hide scroll sliders, and implement custom scroll slider that are (funtionality implemented, make it look good later)~~
    - done!
    - opaque when mouse hovered on it
    - semi transparent when mouse is in window
    - invisible when cursor leaves window 

* write a new hotkey manager (current task) 
    - have a hotkeys changed signa, so widgets can update their bindings when needed.
    - use native api for each plotform (windows, linux like, mac) for monitoring global hotkeys
    - have a system to automatically register hotkeys to qt for local hotkeys
    - the manager itself should hold all the *global*/system wide hotkeys
    - for local hotkeys:
        + ~~binded to a widget only~~
        +~~ manager hold all the details regarding binded keys~~
        +~~widget provide name and a signal to emit when key is pressed~~
        + ~~manager contains the binding name and the keys~~

    * now working on:

        + ~~implement global hotkeys for windows.~~ (finished for windows)