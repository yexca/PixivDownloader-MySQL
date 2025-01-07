from PyQt6.QtWidgets import QMainWindow, QSplitter, QListWidget, QStackedWidget, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QApplication

from app.ui.home_window import HomeWindow
from app.ui.settings_window import SettingsWindow
from app.ui.about_window import AboutWindow
from app.ui.pixiv_auth_window import PixivAuthWindow
from app.utils.conf import Conf

import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.conf = Conf()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.conf.APP_NAME + " v" + self.conf.VERSION)
        # self.setFixedSize(1280, 720)  # 设置窗口大小
        # self.resize(1280, 720)
        screen = QApplication.primaryScreen()
        dpi_scaling = screen.devicePixelRatio()

        scaled_width = int(1280 / dpi_scaling)
        scaled_height = int(720 / dpi_scaling)
        self.resize(scaled_width, scaled_height)

        # 创建 Splitter
        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Horizontal)

        # 左侧菜单栏
        self.menu_list = QListWidget()
        self.menu_list.addItem("首页")
        self.menu_list.addItem("Pixiv 验证")
        self.menu_list.addItem("设置")
        self.menu_list.addItem("关于")
        self.menu_list.currentRowChanged.connect(self.change_page)

        # 右侧内容区
        self.stacked_widget = QStackedWidget()

        # 添加页面
        self.stacked_widget.addWidget(HomeWindow())
        self.stacked_widget.addWidget(PixivAuthWindow())
        self.stacked_widget.addWidget(SettingsWindow())
        self.stacked_widget.addWidget(AboutWindow())

        # 布局
        splitter.addWidget(self.menu_list)
        splitter.addWidget(self.stacked_widget)
        splitter.setStretchFactor(1, 4)

        self.setCentralWidget(splitter)

    def paintEvent(self, event):
        painter = QPainter(self)
        # pixmap = QPixmap(os.getcwd() + "\\app\\resources\\images\\background.png")
        pixmap = QPixmap(self.conf.BGIMG)
        painter.drawPixmap(self.rect(), pixmap)

    def change_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
