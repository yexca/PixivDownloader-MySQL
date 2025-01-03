import os
import requests
import json

class SingleDownload:
    def __init__(self):
        self.settings_path = os.path.join(os.getcwd(), "app", "resources", "conf", "settings.json")
        self.downloadPath = ""
        self.load_settings()
        os.makedirs(self.downloadPath, exist_ok=True)

    def __call__(self, userName: str , userID: str, url: str):
        return self.single_download(userName, userID, url)

    def single_download(self, userName: str , userID: str, url: str) -> bool:
        # 判断画师文件夹是否存在
        save_dir = os.path.join(self.downloadPath, userName + " - " + userID)
        os.makedirs(save_dir, exist_ok=True)

        file_name = url.split("/")[-1]  # 从 URL 中提取文件名
        # save_path = os.path.join(self.downloadPath, userName ,file_name)
        save_path = os.path.join(save_dir, file_name)
        try:
            # 设置 HTTP 请求头（例如，对于 Pixiv 需要 Referer）
            headers = {
                "Referer": "https://www.pixiv.net/",
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
            }
            
            # 发起 GET 请求
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()  # 检查是否请求成功

            # 保存文件
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):  # 分块下载
                    file.write(chunk)
            print(f"File saved to {save_path}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        pass

    def load_settings(self):
        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
            # Populate fields
            self.downloadPath = settings.get("download_path", "")
        except FileNotFoundError:
            print(f"Settings file not found at {self.settings_path}.")
        except json.JSONDecodeError:
            print("Error decoding the settings file.")
