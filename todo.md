
## Stick honey pot todos

* write javascript parser  (current task)
    - try to support type script, since js is a strict subset
* ~~fix bugs regarding window edge drag to scale~~


* hide scroll sliders, and implement custom scroll slider that are 
    - opaque when mouse hovered on it
    - semi transparent when mouse is in window
    - invisible when cursor leaves window 

* implement copying images in preview 

* add convience hotkeys
    - should all be rebinable
    - ctrl 8(*) for wrapping current selection in star once (or currrent line is no selection) (strip space)
    - ctrl I to make selection italic (just wrap * once)
    - ctrl B to make selection Bold (wrapping * twice)
    - ctrl `(~) to cross out current selection (wrap ~ twice)
    - ctrl 3(#) to append 1 # at the beginning of current line
    - maybe a key to make inserting image link or text link quicker, not decided yet.

* write a new hotkey manager
    - use native api for each plotform (windows, linux like, mac) for monitoring global hotkeys
    - have a system to automatically register hotkeys to qt for local hotkeys

* write a new config manager
    - use a json like/python dict like interface to define schema
    - should handle multiple variable types as before
    - self modifying code:
        - generate type hinting file in a meta class to type hint for a default schema layout


