import os
from time import time
from typing import List
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QMimeData, pyqtSignal, QUrl
from PyQt5.QtGui import QImage
from utils import cacheLocation
from random import randint
from hashlib import md5
from urllib.parse import urlparse
from os import path

copyCommand = "copy" if os.name == "nt" else "cp"  # copy for windows, cp for unix systems
backSlash = "\\"


def cleanSlash(d: str):
    """
    replaces all the slashes with whichever the os uses
    """
    return d.replace("\\", os.sep).replace("/", os.sep)


class MarkdownEditor(QTextEdit):
    """
    class used to inject markdown behaviour into a QTextEdit
    """

    fileAddedSignal = pyqtSignal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setAcceptRichText(False)

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

