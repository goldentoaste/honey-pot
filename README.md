# stickyMarkdown
 🍯


## Known issues:
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