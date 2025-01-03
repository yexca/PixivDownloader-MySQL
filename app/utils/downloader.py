from app.utils.single_download import SingleDownload
from app.utils.pixiv import Pixiv

import random
import logging
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
        illusts = self.pixiv.getAllIllustFromUserID(userInfo.get("ID"))

        for illust in illusts:
            self.getDownloadLink(illust)

        logging.debug("Downloader.downloader")

        if userInfo.get("lastDownloadID"):
            for url in self.downloadLink:
                self.rand_sleep()
                if url.split("/")[-1].split("_")[0] < userInfo.get("lastDownloadID"):
                    continue
                self.single_download(userInfo.get("name"), userInfo.get("ID"), url)
        else:
            for url in self.downloadLink:
                self.rand_sleep()
                self.single_download(userInfo.get("name"), userInfo.get("ID"), url)

    def getDownloadLink(self, illust):
        if illust.meta_single_page.original_image_url:
            logging.debug("Downloader.getDownloadLink: 单个图片")
            self.downloadLink.append(illust.meta_single_page.original_image_url)
        elif illust.meta_pages:
            logging.debug("Downloader.getDownloadLink: 多个图片")
            for urls in illust.meta_pages:
                self.downloadLink.append(urls.image_urls.original)

    def rand_sleep(self, base: float = 0.1, rand: float = 2.5) -> None:
        time.sleep(base + rand * random.random())  # noqa: S311
            
