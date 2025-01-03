import sys
import os
from PyQt6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.utils.log_conf import LogConf

def load_stylesheet(file_path):
    # 加载 QSS 样式表
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Stylesheet file not found: {file_path}")
        return ""

# def adjust_qss_with_absolute_path(qss_path, background_image_path):
#     """将背景图片路径写入 QSS 文件"""
#     try:
#         with open(qss_path, "r", encoding="utf-8") as file:
#             qss = file.read()
#         # 替换占位符 {background_image_path} 为图片绝对路径
#         qss = qss.replace("{background_image_path}", background_image_path)
#         return qss
#     except FileNotFoundError:
#         print(f"File not found: {qss_path}")
#         return ""

def main():

    # 日志
    log_conf = LogConf()
    log_conf.setup_logging()    

    app = QApplication(sys.argv)

    # 动态获取 QSS 文件和图片路径
    base_path = os.path.dirname(__file__)
    qss_path = os.path.join(base_path, "app/resources/stylesheets/main.qss")
    # background_image_path = os.path.join(base_path, "resources/images/background.png").replace("\\", "/")

    # app.setStyleSheet(adjust_qss_with_absolute_path(qss_path, background_image_path))
    app.setStyleSheet(load_stylesheet(qss_path))

    # 获取项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    # 将工作目录设置为项目根目录
    os.chdir(project_root)

    # 现在可以使用相对路径加载资源
    # pixmap = QPixmap("resources/images/background.png")

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
