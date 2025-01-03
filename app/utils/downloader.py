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
        self.lastDownloadID = 0

    def __call__(self, userInfo):
        return self.downloader(userInfo)

    def downloader(self, userInfo) -> str:
        illusts = self.pixiv.getAllIllustFromUserID(userInfo.get("ID"))

        for illust in illusts:
            self.getDownloadLink(illust)

        if userInfo.get("lastDownloadID"):
            logging.debug("Downloader.downloader: 数据库有记录")
            for url in self.downloadLink:
                currentDownloadID = int(url.split("/")[-1].split("_")[0])
                if currentDownloadID <= int(userInfo.get("lastDownloadID")):
                    logging.info("这张图片已经下载过了: %s", currentDownloadID)
                    continue
                self.rand_sleep()
                self.single_download(userInfo.get("name"), userInfo.get("ID"), url)
                if self.lastDownloadID < currentDownloadID:
                    self.lastDownloadID = currentDownloadID
        else:
            logging.debug("Downloader.downloader: 数据库无记录")
            for url in self.downloadLink:
                self.rand_sleep()
                currentDownloadID = int(url.split("/")[-1].split("_")[0])
                self.single_download(userInfo.get("name"), userInfo.get("ID"), url)
                if self.lastDownloadID < currentDownloadID:
                    self.lastDownloadID = currentDownloadID
        return str(self.lastDownloadID)

    def getDownloadLink(self, illust):
        if illust.meta_single_page.original_image_url:
            logging.debug("Downloader.getDownloadLink: 单个图片")
            self.downloadLink.append(illust.meta_single_page.original_image_url)
        elif illust.meta_pages:
            logging.debug("Downloader.getDownloadLink: 多个图片")
            for urls in illust.meta_pages:
                self.downloadLink.append(urls.image_urls.original)

    def rand_sleep(self, base: float = 0.1, rand: float = 2.5) -> None:
        random_sleep = base + rand * random.random()
        logging.info("Downloader.rand_sleep: 随机休眠: %s", random_sleep)
        time.sleep(random_sleep)  # noqa: S311
            
