import os
from glob import glob
from time import time
from typing import Dict, Tuple

import requests
from validators import url as isUrl

from requests.exceptions import RequestException
from hashlib import md5
from PySide6.QtGui import QImage, QPixmap

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

    def getFile(self, url: str, noDeleteFlag: bool = False) ->Tuple[str, QImage]:
        # TODO replace loading image from local to save cache in memory for each page, clear the cache for a page when its closed
        """
        takes a web image link and returns a file path, cached
        """
        urlHash = md5(url.encode('ascii')).hexdigest()
        
        # if url is cached, just return it
        try:
            return self.images[urlHash], QImage(self.images[urlHash])
        except KeyError:
            pass

        # try to download the link
        if not isUrl(url):
            print("not an url")
            return None, None

        try:
            result = requests.get(url)
        except RequestException:
            print("Web request failed")
            return None, None

        print(result.headers)
        try:
            mimeType = result.headers["Content-Type"]
            print(f"Content-Type: {mimeType}")
            ext = imageExt[mimeType]
            filePath = os.path.join(self.folder, f"{'nodelete' if noDeleteFlag else''}{urlHash}{ext}")
            with open(filePath, "wb") as out:
                out.write(result.content)
            
            self.images[urlHash] = filePath

            return filePath, QImage.fromData(result.content)
        except KeyError:
            print("link is not an image or content type is not found")
            print(url)
            return None, None

    def removeExtra(self):
        """
        removes the cached images that exceeds cache size limit
        """

        deletableKeys = [key for key, val in self.images.items() if not val.startswith("nodelete")]
        diff = len(deletableKeys) - self.cacheSize
        if diff > 0:
            keysToDelete = deletableKeys[0:diff]
            for key in keysToDelete:
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
