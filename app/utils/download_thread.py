from PyQt6.QtCore import QThread, pyqtSignal
import logging

from app.utils.get_info import GetInfo
from app.utils.downloader import Downloader

class DownloadThread(QThread):
    progress = pyqtSignal(str)  # 信号，传递进度
    finished = pyqtSignal()    # 信号，表示任务完成

    def __init__(self, userID, illustID, parent=None):
        super().__init__(parent)
        self.userID = userID
        self.illustID = illustID

    def run(self):
        self.progress.emit("爬取信息中")
        get_info = GetInfo()
        userInfo = get_info(self.userID, self.illustID)
        logging.debug("获取信息： %s", userInfo)
        self.progress.emit("获取信息完成")

        # 下载
        downloader = Downloader()
        self.progress.emit("下载图片中")
        downloader(userInfo)
        self.progress.emit("下载完成")

        # 返回信号
        self.finished.emit()

