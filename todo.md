
# Sticky honey pot todos 🍯

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

        + implement global hotkeys for windows.

* ConfigManger should generate its gui that modifies itself, base on current schema.    

* Hotkey Manager should generate a gui to edit all the key bindings.


* implement copying images in preview 
* fix/hide QSpliiter when Editor is hidden and exiting editing mode.

* add convience hotkeys
    - should all be rebinable
    - ctrl 8(*) for wrapping current selection in star once (or currrent line is no selection) (strip space)
    - ctrl I to make selection italic (just wrap * once)
    - ctrl B to make selection Bold (wrapping * twice)
    - ctrl `(~) to cross out current selection (wrap ~ twice)
    - ctrl 3(#) to append 1 # at the beginning of current line
    - Tab indents selected text by 1 tab, or until the next 4 space increment
    - ctrl space to insert `&nbsp;` once as non removing space (although it seems like Qt preserves space. :/)
                    - maybe a key to make inserting image link or text link quicker, not decided yet.



* bug fix: remove tabs from end of line highlight

* add emoji support (way later)
    - should respect escaped `\:`
    - cast common emoji like `:/ :) :( ;-;` etc to a unicode emoji, (should be an setting boolean to disable)
    - should show a auto complete widget when typing starting with `:`
        + `:br`->
        + `:bread`
        + `bricks`
        + `brain` etc
        
        sdsaadsad

```
build
nuitka notes.py  --enable-plugin=pyside6 --onefile --standalone  --include-data-dir=GUI=GUI  --windows-disable-console
```

