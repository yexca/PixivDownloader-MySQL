from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QHBoxLayout, QMessageBox
)
from app.utils.get_info import GetInfo
from app.utils.downloader import Downloader

class HomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # 画师 ID
        self.userID_label = QLabel("画师 ID:")
        self.userID_input = QLineEdit()

        # 作品 ID
        self.illustID_label = QLabel("作品 ID:")
        self.illustID_input = QLineEdit()

        # Button
        self.button = QPushButton("开始")
        self.button.clicked.connect(self.startDownload)

        userID_layout = QHBoxLayout()
        userID_layout.addWidget(self.userID_label)
        userID_layout.addWidget(self.userID_input)
        layout.addLayout(userID_layout)

        illustID_layout = QHBoxLayout()
        illustID_layout.addWidget(self.illustID_label)
        illustID_layout.addWidget(self.illustID_input)
        layout.addLayout(illustID_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def startDownload(self):
        try:
            self.button.setEnabled(False)
            self.button.setText("爬取中")
            get_info = GetInfo()

            if get_info == None:
                self.show_warn()

            print("开始获取信息")
            # print(self.userID_input.text())
            # print(self.illustID_input.text())
            userInfo= get_info(self.userID_input.text(), self.illustID_input.text())
            print("获取信息完成")
            self.button.setText("下载中")
            print("开始下载")
            downloader = Downloader()
            downloader(userInfo)
            print("下载完成")
            self.show_info()
            self.button.setEnabled(True)
        except Exception as e:
            print(f"Error in startDownload: {e}")
            self.button.setEnabled(True)
            self.button.setText("开始")

    def show_info(self):
        QMessageBox.information(self, "信息提示", "下载完成！", QMessageBox.StandardButton.Ok)
    def show_warn(self):
        QMessageBox.warning(self, "信息提示", "未输入", QMessageBox.StandardButton.OK)