import os
from glob import glob
from typing import Dict

import requests
import validators
from requests.exceptions import RequestException

imageExt = {"image/bmp": ".bmp", "image/jpeg": ".jpg", "image/png": ".png"}

# NOTE
# save images has <abs(hash(fileURL))>.ext
class CacheManager:
    def __init__(self, cacheFolder: str, cacheSize: int) -> None:

        self.folder = cacheFolder
        self.cacheSize = cacheSize
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
        self.images: Dict[str, str] = {}  # paths to images

        # get .bmp, .jpg, or .png files in the cache folder, sorted by last modified date
        for file in sorted(
            sum((glob(os.path.join(self.folder, f"*{ext}")) for ext in imageExt.values()), start=[]),
            key=os.path.getmtime,
        ):
            self.images[os.path.splitext(file)[0]] = file

    def getFile(self, url: str) -> str:
        """
        takes a web image link and returns a file path, cached
        """

        # if url is cached, just return it
        if str(abs(hash(url))) in self.images:
            return self.images[hash(url)]

        # try to download the link
        if not validators.url(url):
            print("not an url")
            return None

        try:
            result = requests.get(url)
        except RequestException:
            print("Web request failed")
            return None

        try:
            mimeType = result.headers["Content-Type"]
            ext = imageExt[mimeType]
            filePath = os.path.join(self.folder, f"{abs(hash(url))}{ext}")
            with open(filePath, "wb") as out:
                out.write(result.content)
            self.images[str(abs(hash(url)))] = filePath
            self.removeExtra()
            return filePath
        except KeyError:
            print("link is not an image, content type is not found")
            return None

    def removeExtra(self):
        """
        removes the cached images that exceeds cache size limit
        """
        diff = len(self.images) - self.cacheSize
        if diff > 0:
            keys = list(self.images.keys())[0:diff]

            for key in keys:
                os.remove(self.images[key])
                self.images.pop(key)

    def clearCache(self):
        """
        clears the entire cache
        """
        oldSize = self.cacheSize
        self.cacheSize = 0
        self.removeExtra()
        self.cacheSize = oldSize
