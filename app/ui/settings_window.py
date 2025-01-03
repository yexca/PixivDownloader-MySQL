import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.settings_path = os.path.join(os.getcwd(), "app", "resources", "conf", "settings.json")
        self.settings = {}
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        # Layout
        layout = QVBoxLayout()

        # Download Path
        self.download_label = QLabel("下载路径:")
        self.download_path_display = QLabel("")
        self.download_path_display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.download_path_button = QPushButton("选择路径")
        self.download_path_button.clicked.connect(self.select_download_path)

        # Database Address
        self.db_host_label = QLabel("数据库地址:")
        self.db_host_input = QLineEdit()

        # Database Address
        self.db_port_label = QLabel("数据库端口:")
        self.db_port_input = QLineEdit()

        # Database Address
        self.db_user_label = QLabel("数据库用户:")
        self.db_user_input = QLineEdit()

        # Database Address
        self.db_password_label = QLabel("数据库密码:")
        self.db_password_input = QLineEdit()

        # Database name
        self.db_database_label = QLabel("数据库名称:")
        self.db_database_input = QLineEdit()

        # Buttons
        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_settings)

        self.reset_button = QPushButton("重置")
        self.reset_button.clicked.connect(self.load_settings)

        # Adding widgets to layout
        # layout.addWidget(self.download_label)
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.download_label)
        path_layout.addWidget(self.download_path_display)
        path_layout.addWidget(self.download_path_button)
        layout.addLayout(path_layout)

        db_address_layout = QHBoxLayout()
        db_address_layout.addWidget(self.db_host_label)
        db_address_layout.addWidget(self.db_host_input)
        layout.addLayout(db_address_layout)

        db_address_layout = QHBoxLayout()
        db_address_layout.addWidget(self.db_port_label)
        db_address_layout.addWidget(self.db_port_input)
        layout.addLayout(db_address_layout)

        db_address_layout = QHBoxLayout()
        db_address_layout.addWidget(self.db_user_label)
        db_address_layout.addWidget(self.db_user_input)
        layout.addLayout(db_address_layout)

        db_address_layout = QHBoxLayout()
        db_address_layout.addWidget(self.db_password_label)
        db_address_layout.addWidget(self.db_password_input)
        layout.addLayout(db_address_layout)

        db_address_layout = QHBoxLayout()
        db_address_layout.addWidget(self.db_database_label)
        db_address_layout.addWidget(self.db_database_input)
        layout.addLayout(db_address_layout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_settings(self):
        # Load settings from the JSON file.
        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                self.settings = json.load(f)

            # Populate fields
            self.download_path_display.setText(self.settings.get("download_path", ""))
            self.db_host_input.setText(self.settings.get("db_host", ""))
            self.db_port_input.setText(self.settings.get("db_port", ""))
            self.db_user_input.setText(self.settings.get("db_user", ""))
            self.db_password_input.setText(self.settings.get("db_password", ""))
            self.db_database_input.setText(self.settings.get("db_database", ""))

        except FileNotFoundError:
            print(f"Settings file not found at {self.settings_path}.")
        except json.JSONDecodeError:
            print("Error decoding the settings file.")

    def save_settings(self):
        """Save current settings to the JSON file."""
        self.settings["download_path"] = self.download_path_display.text()
        self.settings["db_host"] = self.db_host_input.text()
        self.settings["db_port"] = self.db_port_input.text()
        self.settings["db_user"] = self.db_user_input.text()
        self.settings["db_password"] = self.db_password_input.text()
        self.settings["db_database"] = self.db_database_input.text()

        try:
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            print("Settings saved successfully.")
            self.show_info()
        except Exception as e:
            print(f"Error saving settings: {e}")

    def select_download_path(self):
        """Open a file dialog to select the download path."""
        path = QFileDialog.getExistingDirectory(self, "选择下载路径")
        if path:
            self.download_path_display.setText(path)

    def show_info(self):
        QMessageBox.information(self, "信息提示", "操作成功！", QMessageBox.StandardButton.Ok)
