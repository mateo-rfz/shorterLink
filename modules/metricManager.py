"""
metric manager Module

This module is designed to manage view counts for short links in a MySQL database.
It includes the ability to:
- Create the `metrix` database and `metrix` table
- Add new short links with initial view counts
- Increment view counts for existing short links
- Retrieve view counts for specific short links

Database:
- MySQL (Database: metrix, Table: metrix)

Table: metrix
- id INT AUTO_INCREMENT PRIMARY KEY
- shortLink VARCHAR(255) UNIQUE
- viewCounter INT DEFAULT 0

Author: Mateo-rfz
Date: 2025-03-03
License: GPL-3.0

Dependencies:
Listed in requirements.txt (install with "pip install -r requirements.txt")
- mysql-connector-python

Usage:
    from modules import metrix

    # Add a new short link
    AddItem("example.com/abc").addItem()

    # Increment view count for a short link
    AddView("example.com/abc").addView()

    # Retrieve view count for a short link
    LinkView("example.com/abc").view()
"""

from modules import config
import mysql.connector as mysql


HOST = config.HOST
DBUSERNAME = config.DBUSERNAME
DBPASSWORD = config.DBPASSWORD
DBPORT = config.DBPORT
DBNAME = "metrix"





class _DbCreator : 
    """
    _DbCreator class
    this class is only use for create database in Mysql 
    """
    def createDB() : 
        conn = mysql.connect(host = HOST, 
                     user = DBUSERNAME , 
                     password = DBPASSWORD)

        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS metrix")
        conn.close()








class Database:
    def __init__(self):
        _DbCreator.createDB()
        self.conn = mysql.connect(host=HOST, 
                                  user=DBUSERNAME, 
                                  password=DBPASSWORD, 
                                  database=DBNAME)

    def get_connection(self):
        return self.conn







class LinkView:
    def __init__(self, shortLink):
        self.shortLink = shortLink
        self.db = Database()



    def view(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM metrix 
                WHERE shortLink = %s
            """, (self.shortLink,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            return [False, str(e)]
        finally:
            cursor.close()






class AddView:
    """
    AddView class
    Increments the view count for a given short link.
    If the short link does not exist, it will add it with an initial view count of 1.
    """
    def __init__(self, shortLink):
        self.shortLink = shortLink
        self.db = Database()
        self.__createTable()

    def __createTable(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrix (
                id INT AUTO_INCREMENT PRIMARY KEY,
                shortLink VARCHAR(255) UNIQUE,
                viewCounter INT DEFAULT 0
            )
        """)
        conn.commit()
        cursor.close()




    def addView(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT viewCounter FROM metrix WHERE shortLink = %s
            """, (self.shortLink,))
            result = cursor.fetchone()

            if result:
                new_view = result[0] + 1
                cursor.execute("""
                    UPDATE metrix SET viewCounter = %s WHERE shortLink = %s
                """, (new_view, self.shortLink))
            else:
                cursor.execute("""
                    INSERT INTO metrix (shortLink, viewCounter) VALUES (%s, %s)
                """, (self.shortLink, 1))

            conn.commit()
            return True
        except Exception as e:
            return [False, str(e)]
        finally:
            cursor.close()





class AddItem:
    """
    AddItem class
    Adds a new short link to the 'metrix' table with an initial view count of 0.
    """
    def __init__(self, shortLink):
        self.shortLink = shortLink
        self.db = Database()
        self.__createTable()

    def __createTable(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrix (
                id INT AUTO_INCREMENT PRIMARY KEY,
                shortLink VARCHAR(255) UNIQUE,
                viewCounter INT DEFAULT 0
            )
        """)
        conn.commit()
        cursor.close()





    def addItem(self):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO metrix (shortLink, viewCounter) VALUES (%s, %s)
            """, (self.shortLink, 0))
            conn.commit()
            return True
        except mysql.IntegrityError:
            return [False, "ItemExists"]
        except Exception as e:
            return [False, str(e)]
        finally:
            cursor.close()
