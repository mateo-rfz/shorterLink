import mysql.connector as mysql
from datetime import datetime

from modules import config





HOST = config.HOST
DBUSERNAME = config.DBUSERNAME
DBPASSWORD = config.DBPASSWORD
DBPORT = config.DBPORT










class Database:
    def __init__(self, dbName="views"):
        self.dbName = dbName
        self.createDB()



    def createDB(self):
        conn = mysql.connect(
            host=HOST,
            user=DBUSERNAME,
            password=DBPASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.dbName}")
        conn.close()



    def connect(self):
        return mysql.connect(
            host=HOST,
            user=DBUSERNAME,
            password=DBPASSWORD,
            database=self.dbName
        )




class ViewMng:
    def __init__(self, ip):
        self.ip = ip
        self.conn = Database().connect()
        self.__createTable()

    def __createTable(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS views(
                id INT PRIMARY KEY AUTO_INCREMENT,
                ip VARCHAR(255) UNIQUE,
                time DATETIME
            )
        """)
        self.conn.commit()
        cursor.close()

    def adder(self):
        cursor = self.conn.cursor()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            cursor.execute("""
                SELECT time FROM views WHERE ip = %s
            """, (self.ip,))
            result = cursor.fetchone()

            if result:
                last_view_time = result[0]
                time_diff = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S') - last_view_time
                if time_diff.total_seconds() < 60:
                    return False

            cursor.execute("""
                INSERT INTO views (ip, time)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE time = VALUES(time)
            """, (self.ip, current_time))

            self.conn.commit()
            return True

        except mysql.Error as err:
            return False

        finally:
            cursor.close()
            self.conn.close()
