from app.utils.single_download import SingleDownload
from app.utils.pixiv import Pixiv
from app.utils.random_sleep import RandomSleep

import logging

class Downloader:
    def __init__(self):
        self.downloadLink = []
        self.pixiv = Pixiv()
        self.single_download = SingleDownload()
        self.lastDownloadID = 0
        self.rand_sleep = RandomSleep()

    def start(self, downloadProgess, userInfo) -> str:
        illusts = self.pixiv.getAllIllustFromUserID(userInfo.get("ID"))

        # 报告进度
        downloadProgess("获取链接中")

        for illust in illusts:
            self.getDownloadLink(illust)

        # 报告进度
        total = len(self.downloadLink)
        i = 1

        if userInfo.get("lastDownloadID"):
            logging.debug("Downloader.downloader: 数据库有记录")
            for url in self.downloadLink:
                # 报告进度
                downloadProgess(f"正在下载第 {i} 张, 共 {total} 张")
                i += 1

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
                # 报告进度
                downloadProgess(f"正在下载 {i}, 一共 {total}")
                i += 1

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
