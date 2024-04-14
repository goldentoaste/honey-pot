# stickyMarkdown

 ![notes](docs/note.png)
This project was meant to be a sticky notes app that is similar to Windows's built in notes app, except it takes markdown input. 

## Features
* ...

## Discontinuation 
I spent quite some time into this project but eventually decided it is not worth the time, for the following reasons:
1. Qt's bad support for markdown rendering. Currently Qt supports markdown with it's `TextEdit.setMarkdown` 

## Running the code



## Known issues/draw backs:
- Qt has issues with parsing titles with strike throughs, for example
    * `### ~~stuff~~` will be parsed into just:  ~~stuff~~
    * use Html tags instead if this is super important (html has its own issues, read below)

- Html header tag after list items are treated as a part of the list item. 
    + for example:              
        ```
        * abc
        * xyz
        * last line
        <h1><s>title!</s></h1>
        ```
        will get parsed into:
        <ul>
        <li>abc</li>
        <li>xyz</li>
        <li>last line<span style=" font-size:xx-large; font-weight:600; text-decoration: line-through;">title!</span></li>
        </ul>
    + use a empty # to trick the parser into adding a new line:
        ```
        * abc
        * xyz
        * last line
        #
        <h1><s>title!</s></h1>
        ```
- nested bullets are all rendered with the solid dot, instead of cycling through circle, square etc like proper markdown would.
- tables are rendered with the default html table looks, so.... very ugly.