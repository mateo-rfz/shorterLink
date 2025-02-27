from modules import config , viewManager

import mysql.connector as mysql




HOST = config.HOST
DBUSERNAME = config.DBUSERNAME
DBPASSWORD = config.DBPASSWORD
DBPORT = config.DBPORT






class _DbCreator : 
    def createDB() : 
        conn = mysql.connect(host = HOST, 
                     user = DBUSERNAME , 
                     password = DBPASSWORD)

        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS mainPmetrix")
        conn.close()








class Database:
    def __init__(self, dbName="mainPmetrix"):
        _DbCreator.createDB()
        self.dbName = dbName

    def connect(self):
        return mysql.connect(
            host=HOST,
            user=DBUSERNAME,
            password=DBPASSWORD,
            database=self.dbName
        )








class LinksCounter:
    def __init__(self):
        self.db = Database()
        self.__createTable()

    def __createTable(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS linksCounter (
                id INT PRIMARY KEY AUTO_INCREMENT,
                count INT DEFAULT 0
            )
        """)
        cursor.execute("""
            INSERT INTO linksCounter (id, count) 
            VALUES (1, 0) 
            ON DUPLICATE KEY UPDATE count = count;
        """)
        conn.commit()
        conn.close()




    def addToLinkCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE linksCounter SET count = count + 1 WHERE id = 1")
        conn.commit()
        conn.close()


    def showLinksCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM linksCounter WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0







class Views:
    def __init__(self , ip = "127.0.0.1"):
        self.db = Database()
        self.__createTable()
        
        self.ip = ip



    def __createTable(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS viewsCounter (
                id INT PRIMARY KEY AUTO_INCREMENT,
                count INT DEFAULT 0
            )
        """)
        cursor.execute("""
            INSERT INTO viewsCounter (id, count) 
            VALUES (1, 0) 
            ON DUPLICATE KEY UPDATE count = count;
        """)
        conn.commit()
        conn.close()



    def addToViewsCounter(self):
        if not viewManager.ViewMng(self.ip).adder() : 
            return False


        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE viewsCounter SET count = count + 1 WHERE id = 1")
        conn.commit()
        conn.close()



    def showViewsCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM viewsCounter WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0










class Users:
    def __init__(self):
        self.db = Database()
        self.__createTable()



    def __createTable(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usersCounter (
                id INT PRIMARY KEY AUTO_INCREMENT,
                count INT DEFAULT 0
            )
        """)
        cursor.execute("""
            INSERT INTO usersCounter (id, count) 
            VALUES (1, 0) 
            ON DUPLICATE KEY UPDATE count = count;
        """)
        conn.commit()
        conn.close()




    def addToUsersCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE usersCounter SET count = count + 1 WHERE id = 1")
        conn.commit()
        conn.close()



    def showUsersCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM usersCounter WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0
