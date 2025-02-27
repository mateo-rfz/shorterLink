import random
import mysql.connector as mysql
import string

from modules import metricManager
from modules import mainPageMetric
from modules import config




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
        cursor.execute("CREATE DATABASE IF NOT EXISTS links")
        conn.close()








class AddUrl:
    def __init__(self, email, originLink, shortLink=None):
        _DbCreator.createDB()

        self.conn = mysql.connect(host=HOST,
                                   user=DBUSERNAME,
                                     password=DBPASSWORD,
                                       database="links")



        self.email = email
        self.originLink = originLink
        self.allchars = string.ascii_letters + string.digits

        if shortLink is None:
            self.shortLink = self.__createRandomShortLink()
        else:
            self.shortLink = shortLink if not self.__checkUrlExistence(shortLink) else False


    def __checkUrlExistence(self, targetUrl):
        self.__createTable()
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM links WHERE shortLink = %s", (targetUrl,))
        result = cursor.fetchone()
        return result is not None

    def __createRandomShortLink(self):
        while True:
            shortLink = "".join(random.choices(self.allchars, k=5))
            if not self.__checkUrlExistence(shortLink):
                return shortLink

    def __createTable(self):
        
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS links(
                id INT PRIMARY KEY AUTO_INCREMENT,
                email VARCHAR(255),
                originLink TEXT,
                shortLink VARCHAR(255) UNIQUE
            )
        """)
        self.conn.commit()

    def __addToDb(self):
        self.__createTable()
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO links (email, originLink, shortLink) 
            VALUES (%s, %s, %s)
        """, (self.email, self.originLink, self.shortLink))
        self.conn.commit()
        self.conn.close()

        metricManager.AddItem(self.shortLink).addItem()
        mainPageMetric.LinksCounter().addToLinkCounter()

        return self.shortLink   

    def add(self):
        if not self.shortLink:
            return False
        return self.__addToDb()







class DelUrl:
    def __init__(self, shortLink):
        _DbCreator.createDB()
        self.shortLink = shortLink
        self.conn = mysql.connect(host=HOST,
                                   user=DBUSERNAME,
                                     password=DBPASSWORD,
                                       database="links")

    def delete(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM links WHERE shortLink = %s", (self.shortLink,))
            self.conn.commit()
            return True
        except Exception as e:
            return [False, e]
        finally:
            self.conn.close()









class ShowUrlWithShortLink:
    def __init__(self, shortLink):
        _DbCreator.createDB()
        self.shortLink = shortLink
        self.conn = mysql.connect(host=HOST,
                                   user=DBUSERNAME,
                                     password=DBPASSWORD,
                                       database="links")

    def show(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT originLink FROM links WHERE shortLink = %s", (self.shortLink,))
            result = cursor.fetchone()
            self.conn.close()
            return result[0] if result else False
        except Exception as e:
            return False








class ShortUrlWithEmail:
    def __init__(self, email):
        _DbCreator.createDB()
        
        self.email = email
        self.conn = mysql.connect(host=HOST,
                                   user=DBUSERNAME,
                                     password=DBPASSWORD,
                                       database="links")

    def show(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM links WHERE email = %s", (self.email,))
            result = cursor.fetchall()
            self.conn.close()
            return result if result else False
        except Exception as e:
            return False
