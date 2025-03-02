"""
View Management Module

This module is responsible for managing and storing IP-based view records in a MySQL database. 
It includes functionalities for creating databases and tables, and adding or updating view records.

Database:
- Database name: views
- Table: views (id, ip, time)

Classes:
- Database: Handles database creation and connection.
- ViewMng: Manages IP-based view records, ensuring duplicate IPs are updated rather than re-inserted.

Author: Mateo-rfz
Date: 2025-03-02
License: GPL-3.0

Dependencies:
- mysql-connector-python
- datetime

Usage:
    from modules import viewManager

    view = ViewMng(ip="192.168.1.1").adder()
"""


import mysql.connector as mysql
from datetime import datetime

#all database connection info on config.py
from modules import config





HOST = config.HOST
DBUSERNAME = config.DBUSERNAME
DBPASSWORD = config.DBPASSWORD
DBPORT = config.DBPORT










class Database:
    """ 
    _DbCreator class
    lass is only use for create database in Mysql 
    """
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
    """
    ViewMng Class

    Manages IP-based view records in the 'views' table. 

    Methods:
    - __init__(ip: str): Initializes the class, establishes a database connection, and creates the 'views' table if it doesn't exist.
    - __createTable() -> None: Creates the 'views' table with columns for id, ip, and time.
    - adder() -> bool: Adds a new view record or updates the timestamp for an existing IP. 
                       Prevents adding duplicate records within a 60-second timeframe.
    """
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
