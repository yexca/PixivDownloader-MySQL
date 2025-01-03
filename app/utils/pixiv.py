from pixivpy3 import *
import json
import os

class Pixiv():
    def __init__(self):
        self.api = AppPixivAPI()
        self.refreshToken = ""
        self.__getToken()
        self.api.auth(refresh_token=self.refreshToken)

    def __getToken(self):
        settings_path = os.path.join(os.getcwd(), "app", "resources", "conf", "settings.json")

        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)

            # Populate fields
            self.refreshToken = settings.get("refresh_token", "")

        except FileNotFoundError:
            print(f"Settings file not found at {settings_path}.")
        except json.JSONDecodeError:
            print("Error decoding the settings file.")
        pass

    def getUserIDFromillustID(self, illustID: str) -> str:
        json_result = self.api.illust_detail(illustID)
        illust = json_result.illust
        userID = illust.user.id
        
        return userID
    
    def getUsernameFromillustID(self, illustID: str) -> str:
        json_result = self.api.illust_detail(illustID)
        illust = json_result.illust
        username = illust.user.name
        
        return username
    
    def getAllIllustFromUserID(self, userID: str):
        json_result = self.api.user_illusts(userID)
        illusts = json_result.illusts
        return illusts
