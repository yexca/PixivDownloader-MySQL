from PyQt6.QtCore import QThread, pyqtSignal
import logging

from app.utils.get_info import GetInfo
from app.utils.downloader import Downloader
from app.utils.sql_connector import SQLConnector

class DownloadThread(QThread):
    progress = pyqtSignal(str)  # 信号，传递进度
    finished = pyqtSignal()    # 信号，表示任务完成

    def __init__(self, userID, illustID, parent=None):
        super().__init__(parent)
        self.userID = userID
        self.illustID = illustID

    def run(self):
        self.progress.emit("查询数据库中")
        get_info = GetInfo()
        userInfo = get_info(self.userID, self.illustID)
        logging.debug("DownloadThread: 获取信息: %s", userInfo)
        self.progress.emit("获取信息完成")

        # 下载
        downloader = Downloader()
        logging.debug("DownloadThread: 下载图片")
        self.progress.emit("准备下载图片")
        lastDownloadID = downloader.start(self.downloadProgess, userInfo)
        self.progress.emit("下载完成")

        # 插入数据库
        logging.debug("DownloadThread: 开始插入数据库")
        self.progress.emit("开始插入数据库")
        userInfo["lastDownloadID"] = lastDownloadID
        sqlConnector = SQLConnector()
        sqlConnector.insertByID(userInfo)
        self.progress.emit("插入数据库完成")

        # 返回信号
        logging.debug("DownloadThread: 返回信号")
        self.finished.emit()

    def downloadProgess(self, value):
        self.progress.emit(value)
