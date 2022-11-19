
## Sticky honey pot todos 🍯

* write javascript parser  (current task)
    - try to support type script, since js is a strict subset
* ~~fix bugs regarding window edge drag to scale~~


* hide scroll sliders, and implement custom scroll slider that are 
    - opaque when mouse hovered on it
    - semi transparent when mouse is in window
    - invisible when cursor leaves window 

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

* write a new hotkey manager
    - use native api for each plotform (windows, linux like, mac) for monitoring global hotkeys
    - have a system to automatically register hotkeys to qt for local hotkeys

* write a new config manager
    - use a json like/python dict like interface to define schema
    - should handle multiple variable types as before
    - self modifying code:
        - generate type hinting file in a meta class to type hint for a default schema layout


* additional markdown syntax highlights
    - ~~highight double space at the end of line to indicate line break~~
    - ~~highlight `\n` on its own line, also linebreak~~ (will ignore for now)
    - ~~highlight tab indents at the beginning~~

* add emoji support
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
nuitka notes.py --standalone --enable-plugin=pyside6 --onefile --windows-disable-console     
```