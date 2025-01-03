# import mysql.connector
# from mysql.connector import Error
import pymysql
import json
import os
import logging

import pymysql.cursors

class SQLConnector():
    def __init__(self):
        print("SQLConnector: 初始化")
        self.settings_path = os.path.join(os.getcwd(), "app", "resources", "conf", "settings.json")
        self.db_settings = {}
        self.__connection = None
        print("SQLConnector: 开始读取配置")
        self.__load_info()
        print("SQLConnector: 读取配置完成")
        # print("SQLConnector: 开始连接数据库")
        # self.__connect_sql()
        # print("SQLConnector: 连接数据库完成")

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
            host = self.db_settings.get("db_host", "")
            port = int(self.db_settings.get("db_port", ""))
            user = self.db_settings.get("db_user", "")
            password = self.db_settings.get("db_password", "")
            database = self.db_settings.get("db_database", "")

            logging.info("开始尝试连接数据库, 连接信息:")
            print(host, port, user, password, database)
            
            # self.__connection = mysql.connector.connect(
            #     host = host,
            #     port = port,
            #     user = user,
            #     password = password,
            #     database = database
            # )

            # 使用 PyMySQL
            self.__connection = pymysql.connect(
                host= host,
                port= port,
                user= user,
                password= password,
                database= database
            )

            # if self.__connection.is_connected():
            if self.__connection.open:
                logging.info("数据库连接成功")
            else:
                logging.error("数据库连接失败")
        except pymysql.MySQLError as e:
            print(f"数据库连接错误: {e}")

    def selectFromID(self, userID: str):
        logging.debug("SQLConnector.selectFromID 开始执行")
        self.__connect_sql()
        logging.debug("SQLConnector.selectFromID 连接成功")
        if self.__connection.open:
            logging.debug("SQLConnector.selectFromID 成功连接至数据库")
            # cursor = self.__connection.cursor(dictionary=True) # dictionary=True 用于返回字典形式的结果

            cursor = self.__connection.cursor(pymysql.cursors.DictCursor) # PyMySQL 用于返回字典形式的结果

            # 查询语句
            sql_select = "select * from pic where id = %s"
            # 执行查询
            cursor.execute(sql_select, (userID,))
            # 获取查询结果
            result = cursor.fetchone() # fetchone() 返回一行数据

            logging.debug("SQLConnector.selectFromID 关闭数据库连接")
            cursor.close()

            if result:
                return result
            else:
                return None
        else:
            logging.warning("连接数据库失败")
