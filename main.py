import sys
import os
from PyQt6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.utils.log_conf import LogConf
from app.utils.style import MAIN_STYLE

def main():
    # Qt APP
    app = QApplication(sys.argv)

    # 日志
    log_conf = LogConf()
    log_conf.setup_logging()   

    app.setStyleSheet(MAIN_STYLE)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
