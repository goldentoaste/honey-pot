import os
from typing import Dict, List
import requests
from requests.exceptions import RequestException
from glob import glob
import validators


imageExt = {"image/bmp": ".bmp", "image/jpeg": ".jpg", "image/png": ".png"}


class CacheManager:
    def __init__(self, cacheFolder: str, cacheSize: int) -> None:

        self.folder = cacheFolder
        self.cacheSize = cacheSize
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
        self.images: Dict[str, str] = {}  # paths to images

        for file in sum([glob(os.path.join(self.folder, f"*{ext}")) for ext in imageExt.values()], start=[]):
            self.images[hash(file)] = file

    def getFile(self, url: str) -> str:
        """
        takes a web image link and returns a file path, cached
        """

        # if url is cached, just return it
        if hash(url) in self.images:
            return self.images[hash(url)]

        # try to download the link
        if not validators.url(url):
            print("not an url")
            return None

        try:
            result = requests.get(url)
        except RequestException:
            print("Web request failed")
            return
        try:
            mimeType = result.headers["Content-Type"]
            ext = imageExt[mimeType]

        except KeyError:
            print("link is not an image")
            return None
