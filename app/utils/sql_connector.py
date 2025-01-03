import mysql.connector
from mysql.connector import Error
import json
import os

class SQLConnector:
    def __init__(self):
        self.settings_path = os.path.join(os.getcwd(), "app", "resources", "conf", "settings.json")
        self.db_settings = {}
        self.__connection = None
        self.__load_info()
        self.__connect_sql()

    def __load_info(self):
        try:
            with open(self.settings_path, "r", encoding="utf-8") as f:
                self.db_settings = json.load(f)
        except FileNotFoundError:
            print(f"Settings file not found at {self.settings_path}.")
        except json.JSONDecodeError:
            print("Error decoding the settings file.")

    def __connect_sql(self):
        try:
            self.__connection = mysql.connector.connect(
                host = self.db_settings.get("db_host", ""),
                port = self.db_settings.get("db_port", ""),
                user = self.db_settings.get("db_user", ""),
                password = self.db_settings.get("db_password", ""),
                database = self.db_settings.get("db_database", "")
            )

            if self.__connection.is_connected():
                # 成功连接数据库
                cursor = self.__connection.cursor(dictionary=True)
        except Error as e:
            print(f"数据库连接错误: {e}")
        finally:
            if self.__connection.is_connected():
                cursor.close()
                self.__connection.close()
                print("数据库连接已关闭")

    def selectFromID(self, userID: str):
        if self.__connection.is_connected():
            print("成功连接至数据库")
            cursor = self.__connection.cursor(dictionary=True) # dictionary=True 用于返回字典形式的结果

            # 查询语句
            sql_select = "select * from pic where id = %s"
            # 执行查询
            cursor.execute(sql_select, (userID,))
            # 获取查询结果
            result = cursor.fetchone() # fetchone() 返回一行数据

            if result:
                return result
            else:
                return None
        else:
            print("连接数据库失败")
