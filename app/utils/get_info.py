from app.utils.sql_connector import SQLConnector
from app.utils.pixiv import Pixiv

import logging

class GetInfo():
    def __init__(self):
        logging.debug("GetInfo: 开始初始化")
        self.pixiv = Pixiv()
        logging.debug("GetInfo: 初始化完成 Pixiv")
        self.sqlConnector = SQLConnector()
        logging.debug("GetInfo: 初始化完成 SQLConnector")

    def __call__(self, userID: str | None = None, illustID: str | None = None):
        return self.get_Info(userID, illustID)
    
    def get_Info(self, userID: str | None = None, illustID: str | None = None):
        logging.debug("GetInfo.get_Info: 查询数据库")
        # if userID != None:
        if userID:
            logging.debug("GetInfo.get_Info: 有用户 ID: %s", userID)
            userInfo = self.sqlConnector.selectFromID(userID)
        elif illustID:
            logging.debug("GetInfo.get_Info: 无用户 ID")
            userID = self.pixiv.getUserIDFromillustID(illustID)
            logging.debug("GetInfo.get_Info: 查询用户 ID: %s", userID)
            userInfo = self.sqlConnector.selectFromID(userID)
        else:
            logging.debug("GetInfo.get_Info: 用户未输入")
            return None
        
        logging.debug("GetInfo.get_Info: 数据库查询完成")

        # 数据库返回部分
        if userInfo:
            logging.debug("GetInfo.get_Info: 数据库有返回, 直接返回")
            return userInfo
        else:
            logging.debug("GetInfo.get_Info: 数据库无返回, 构造返回")
            userInfo = {}
            userInfo["ID"] = userID
            logging.debug("GetInfo.get_Info: 构造信息 userID: %s", userID)
            userInfo["name"] = self.pixiv.getUsernameFromuserID(userID)
            logging.debug("GetInfo.get_Info: 构造信息完成")
            return userInfo
        
