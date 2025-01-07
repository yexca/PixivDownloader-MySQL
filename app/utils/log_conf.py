import logging
import logging.config
import os
import sys

class LogConf():
    def __init__(self):
        # 如果是打包后的可执行文件，获取其目录；否则获取源代码目录
        base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        # 设置日志文件路径
        LOG_DIR = os.path.join(base_dir, "logs")
        LOG_FILE_PATH = os.path.join(LOG_DIR, "app_logs.log")
        
        # 确保日志目录存在
        os.makedirs(LOG_DIR, exist_ok=True)
        self.logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                },
                "file": {
                    "level": "INFO",
                    "class": "logging.FileHandler",
                    "formatter": "standard",
                    "filename": LOG_FILE_PATH,
                    "encoding": "utf-8",  # 确保文件以 UTF-8 编码写入
                },
            },
            "root": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
            },
            "loggers": {
                "sql_logger": {
                    "level": "INFO",
                    "handlers": ["file"],
                    "propagate": False,
                },
            },
        }

    def setup_logging(self):
        logging.config.dictConfig(self.logging_config)

# 记录不同级别的日志
# logging.debug("This is a debug message.")
# logging.info("This is an info message.")
# logging.warning("This is a warning message.")
# logging.error("This is an error message.")
# logging.critical("This is a critical message.")

