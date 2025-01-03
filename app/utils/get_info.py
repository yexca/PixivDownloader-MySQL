from app.utils.sql_connector import SQLConnector
from app.utils.pixiv import Pixiv

class GetInfo:
    def __init__(self):
        self.pixiv = Pixiv()
        self.sqlConnector = SQLConnector()
        pass

    def __call__(self, userID: str | None = None, illustID: str | None = None):
        return self.get_Info(userID, illustID)
    
    def get_Info(self, userID: str | None = None, illustID: str | None = None):
        userInfo = {}
        if userID != None:
            userInfo = self.sqlConnector.selectFromID(userID)
        elif illustID != None:
            userID = self.pixiv.getUserIDFromillustID(illustID)
            userInfo = self.sqlConnector.selectFromID(userID)
        else:
            print("用户未输入")
            return None
        
        # 返回部分
        if userInfo:
            return userInfo
        else:
            userInfo["ID"] = userID
            userInfo["name"] = self.pixiv.getUsernameFromillustID(illustID)
