import html
import os
import textwrap
from hashlib import md5
from os import path
from random import randint
from time import time
from typing import List

from PySide6.QtCore import QMimeData, QSize, Qt, QUrl, Signal, Slot
from PySide6.QtGui import (QImage, QKeyEvent, QKeySequence, QShortcut,
                           QTextCursor)
from PySide6.QtWidgets import QPlainTextEdit, QTextBrowser, QTextEdit

from Hotkeys.keyConfig import Bold, Italic, Wrapstars, Strikethrough, Title, Htmlspace, getKeyConfig
from imageCache import CacheManager
from syntaxHighlighting import EditorHighlighter, Languages, PreviewHighlighter
from transparentScrollbar import TransScrollBar
from utils import cacheLocation, mdCodeBlockRegex, mdImageRegex

copyCommand = "copy" if os.name == "nt" else "cp"  # copy for windows, cp for unix systems
backSlash = "\\"


def cleanSlash(d: str):
    """
    replaces all the slashes with whichever the os uses
    """
    return d.replace("\\", os.sep).replace("/", os.sep)


class MarkdownPreview(QTextBrowser):

    fileAddedSignal = Signal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cache = CacheManager(r"C:\\Testing\\cache", 5)
        self.blockTypes = []  # python, text, etc
        self.allBlockTypes = {
            "python": Languages.python,
            "py": Languages.python,
            "js": Languages.javascript,
            "javascript": Languages.javascript,
            "text": Languages.text,
            "txt": Languages.text,
        }

        self.langHeaderMap = {
            Languages.text: "\u200b",
            Languages.python: "\u200b\u200b",
            Languages.javascript: "\u200b\u200b\u200b",
        }

        self.highlighter = PreviewHighlighter(self.document())
        self.document().setIndentWidth(20)

        self.keys = QShortcut(
            QKeySequence(
                "Ctrl+.",
            ),
            self,
        )
        self.keys.activated.connect(lambda: print("test"))
        # Set style

        self.setStyleSheet(
            """
            QTextEdit{border:1px solid #000000;}
            """
        )

        self.vertScrollBar = TransScrollBar(Qt.Orientation.Vertical, self.parent(), self)
        self.horScrollBar = TransScrollBar(Qt.Orientation.Horizontal, self.parent(), self)

    def setMarkdown(self, markdown: str) -> None:
        # fixing code blocks
        "========================================================"
        t0 = time()
        self.blockTypes.clear()
        codeBlocks = mdCodeBlockRegex.findall(markdown)
        block: str
        for block in codeBlocks:
            langHeader = block[: block.find("\n")]
            langType = self.allBlockTypes.get(langHeader, Languages.text)
            block = block[block.find("\n") + 1 :]
            block = textwrap.indent(html.escape(block).strip("\n").replace("\\", "\\\\"), "    ")
            markdown = mdCodeBlockRegex.sub(
                f'<pre style="background-color:#292828;color:#d4be98;">\n<p1 style="font-size: 10pt; font-family: Comic Sans MS; ">\n\n{self.langHeaderMap[langType]}{block}\u200c\n</p1></pre>',
                markdown,
                1,
            )
        print("code block processing took", time() - t0)
        "========================================================"

        t0 = time()
        super().setMarkdown(markdown)
        print(f"setting markdown took: {time() - t0}")

        # loading images
        "========================================================"
        t0 = time()
        imageLinks = mdImageRegex.findall(markdown)
        for link in imageLinks:
            cachedFile, image = self.cache.getFile(link)
            if cachedFile:
                self.document().addResource(2, QUrl(link), image)
        print(f"image handling took: {time() - t0}")
        "========================================================"

        # # adjust size of contents
        # self.document().adjustSize()


class MarkdownEditor(QPlainTextEdit):
    """
    class used to inject markdown behaviour into a QTextEdit
    """

    fileAddedSignal = Signal(str)

    wrapStarsSig = Signal()
    boldSig = Signal()
    strikeThrough = Signal()
    title = Signal()
    space = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.highlighter = EditorHighlighter(self.document())

        key = getKeyConfig()
        key.bindLocal(Wrapstars, self, self.wrapStarsSig, Qt.ShortcutContext.WidgetWithChildrenShortcut)
        key.bindLocal(Italic, self, self.wrapStarsSig, Qt.ShortcutContext.WidgetWithChildrenShortcut)
        key.bindLocal(Bold, self, self.boldSig, Qt.ShortcutContext.WidgetWithChildrenShortcut)
        key.bindLocal(Strikethrough, self, self.strikeThrough, Qt.ShortcutContext.WidgetWithChildrenShortcut)
        key.bindLocal(Title, self, self.title, Qt.ShortcutContext.WidgetWithChildrenShortcut)
        key.bindLocal(Htmlspace, self, self.space, Qt.ShortcutContext.WidgetWithChildrenShortcut)
        
        self.wrapStarsSig.connect(lambda:self.wrapWithChars("*", 1)) 
        self.boldSig.connect(lambda:self.wrapWithChars("*", 2)) 
        self.strikeThrough.connect(lambda:self.wrapWithChars("~", 2)) 
        self.title.connect(self.insertAtBeginning)
        self.space.connect(self.insertAtCursor("&nbsp", 1))

    def canInsertFromMimeData(self, source: QMimeData) -> bool:
        return super().canInsertFromMimeData(source)

    def createMimeDataFromSelection(self) -> QMimeData:
        return super().createMimeDataFromSelection()

    def insertFromMimeData(self, source: QMimeData) -> None:
        print(source.formats())
        print("has images", source.hasImage())
        print("has urls/uris", source.hasUrls(), source.urls())

        if source.hasImage():
            """
            save image data to cache, then some how replace image data with local link to the cached image
            """
            imagedata: QImage = source.imageData()
            if not imagedata:
                return

            imagePath = path.join(
                cacheLocation, md5(f"{time()}{randint(0, 999)}".encode("ascii")).hexdigest() + ".jpg"
            )
            imagedata.save(imagePath, "JPG", 85)
            self.fileAddedSignal.emit(imagePath)
            return self.insertPlainText(f"![pasted image]({imagePath})")

        if source.hasUrls():  # prob a local file
            urls: List[QUrl] = source.urls()
            for url in urls:
                # only checking uris starting with "file:///" or uris pointing to local files
                if (
                    url.isLocalFile()
                ):  # BUG just checking for isLocalFile() aka "file://" header is not enough, could be a network file
                    imagePath = url.path().strip("/").strip("\\")
                    print(f"parsed uri path: {imagePath}")
                    if not imagePath.endswith((".jpg", ".png", ".bmp", ".jpeg")):
                        return  # ignore non image files

                    _, ext = path.splitext(imagePath)
                    imageName = path.basename(imagePath)
                    newPath = path.join(cacheLocation, md5(imageName.encode("ascii")).hexdigest() + ext)
                    print(f"image destination: {newPath}")
                    if not path.isfile(newPath):
                        os.system(f'{copyCommand} "{cleanSlash(imagePath)}" "{cleanSlash(newPath)}"')

                    self.fileAddedSignal.emit(newPath)
                    return self.insertPlainText(f"![{imageName}]({newPath})")

                else:
                    print(f"url is not a local file uri: {url}")

        return super().insertFromMimeData(source)

    def insertAtCursor(self, chars="*", n=1):
        cursor = self.textCursor()
        cursor.insertText(chars * n)
        self.setTextCursor(cursor)

    def wrapWithChars(self, char="*", n=1):
        """
        wrap selected text with char, n times.
        if no text is selected, try to wrap the wholeline, then place the cursor infront
        of the ending char group: text text text -> **text text text<cursor here>**
        """
        cursor: QTextCursor = self.textCursor()
        cursor.beginEditBlock()
        print("in wrap stars")
        if cursor.hasSelection():
            
            start = cursor.selectionStart()
            end = cursor.selectionEnd()
            # start with end, so start is not effect
            cursor.setPosition(end)
            cursor.insertText(char * n)
            cursor.setPosition(start)
            cursor.insertText(char * n)
            
            cursor.setPosition(end +n, QTextCursor.MoveMode.KeepAnchor)
        else:
            # apply to whole line here
            cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock, QTextCursor.MoveMode.MoveAnchor)
            cursor.insertText(char * n)
            start = cursor.position()
            cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.MoveAnchor)
            end  = cursor.position()
            cursor.insertText(char * n)
            
            cursor.setPosition(end)
            cursor.setPosition(start, QTextCursor.MoveMode.KeepAnchor)
        cursor.endEditBlock()
        self.setTextCursor(cursor)
            
            
    def insertAtBeginning(self, char="#", n=1):
        
        cursor = self.textCursor()
        cursor.beginEditBlock()
        pos = cursor.position()
        
        cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
        cursor.insertText(char * n)
        
        if not cursor.atBlockEnd():
            cursor.setPosition(cursor.position() + 1, QTextCursor.MoveMode.KeepAnchor)
            t= cursor.selectedText()
            if t != " " and t !="#":
                cursor.setPosition(cursor.position() - 1)
                cursor.insertText(" ")
                n += 1
        
        cursor.setPosition(pos + n)
        self.setTextCursor(cursor)
        cursor.endEditBlock()