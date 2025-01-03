from app.utils.single_download import SingleDownload
from app.utils.pixiv import Pixiv

import random
import time

class Downloader:
    def __init__(self):
        self.downloadLink = []
        self.pixiv = Pixiv()
        self.single_download = SingleDownload()
        pass

    def __call__(self, userInfo):
        return self.downloader(userInfo)

    def downloader(self, userInfo):
        illusts = self.pixiv.getAllIllustFromUserID(userInfo.ID)

        for illust in illusts:
            self.getDownloadLink(illust)

        if userInfo.lastDownloadID:
            for url in self.downloadLink:
                self.rand_sleep()
                if url.split("/")[-1].split("_")[0] < userInfo.lastDownloadID:
                    continue
                self.single_download(userInfo.name, url)
        else:
            for url in self.downloadLink:
                self.rand_sleep()
                self.single_download(userInfo.name, url)

    def getDownloadLink(self, illust):
        if illust.meta_single_page.original_image_url:
            print("单个图片")
            self.downloadLink.append(illust.meta_single_page.original_image_url)
        elif illust.meta_pages:
            print("多个图片")
            for urls in illust.meta_pages:
                self.downloadLink.append(urls.image_urls.original)

    def rand_sleep(self, base: float = 0.1, rand: float = 2.5) -> None:
        time.sleep(base + rand * random.random())  # noqa: S311
            
