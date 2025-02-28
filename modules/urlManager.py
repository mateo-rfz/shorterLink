"""
URL Manager Module

This module is designed to manage URLs by providing functionalities such as:
- Adding a new SHORT-URL + ORIGIN-URL
- Deleting a SHORT-URL + ORIGIN-URL
- Searching for OriginUrl with ShortUrl
- Searching for OriginUrl and ShortUrl with Email

Database:
- MySQL (Database: links, Table: users)

It links MySQL for data management with the following structure:

Database: links  
Table: users  
- id INT PRIMARY KEY AUTO_INCREMENT,
- email VARCHAR(255),
- originLink TEXT,
- shortLink VARCHAR(255) UNIQUE


Author: Mateo-rfz
Date: 2025-02-28  
License: GPL-3.0

Dependencies:
listed on requirements.txt (install with "pip install -r requirements.txt")
- mysql-connector-python
- random
- string

Usage:
    from modules import urlManager

    #add new url with email originLink and shortLink
    urlManager.AddUrl(email , originLink , shortLink).add()

    #delete url with shortLink
    urlManager.DelUrl(shortLink).delete()

    #find the origin url with shortLink
    urlManager.ShowUrlWithShortLink(shortLink).show()

    #find the origin url + short url with email
    urlManager.ShortUrlWithEmail(email).show()
"""





#use random and string for create random shortLink
import random
import string


import mysql.connector as mysql


from modules import metricManager
from modules import mainPageMetric

#all database connection info on config.py
from modules import config




HOST = config.HOST
DBUSERNAME = config.DBUSERNAME
DBPASSWORD = config.DBPASSWORD
DBPORT = config.DBPORT






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
        cursor.execute("CREATE DATABASE IF NOT EXISTS links")
        conn.close()








class AddUrl:
    """
    AddUrl class

    This class is responsible for adding URLs to the database using the provided 
    email, original link, and short link.

    If shortLink is None, a random 5-character string will be generated as the short link.


    Methods : 
    - __checkUrlExistence -> bool : check url existence for if url existence return error.
    - __createRandomShortLink -> string : Generates a random 5-character string to use as a shortLink.
    - __createTable : use for create 'links' table in Mysql (IF NOT EXISTS).
    - __addToDb -> bool : this method is use for push to database datas.
    - add : the main method for this class use for return __addToDb answer.

    """
    def __init__(self, email : str , originLink : str , shortLink=None):
        _DbCreator.createDB()

        self.conn = mysql.connect(host=HOST,
                                   user=DBUSERNAME,
                                     password=DBPASSWORD,
                                       database="links")



        self.email = email.lower()
        self.originLink = originLink
        self.allchars = string.ascii_letters + string.digits

        if shortLink is None:
            self.shortLink = self.__createRandomShortLink()
        else:
            self.shortLink = shortLink if not self.__checkUrlExistence(shortLink) else False
            self.shortLink = self.shortLink.lower()


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
    """
    DelUrl class

    This class is responsible for Delete URLs to the database using the shortLink.


    Methods : 
    - __checkUrlExistence -> bool : check url existence for if url existence return error.
    - __createRandomShortLink -> string : Generates a random 5-character string to use as a shortLink.
    - __createTable : use for create 'links' table in Mysql (IF NOT EXISTS).
    - __addToDb -> bool : this method is use for push to database datas.
    - add : the main method for this class use for return __addToDb answer.

    """
    def __init__(self, email : str , shortLink : str):
        _DbCreator.createDB()
        self.shortLink = shortLink
        self.email = email

        self.conn = mysql.connect(host=HOST,
                                   user=DBUSERNAME,
                                     password=DBPASSWORD,
                                       database="links")
        
    def __checkShortLinkOwner(self) :
        urlOwnerEmail = ShowUrlWithShortLink(self.shortLink , byEmail = True).show()[1]
        if urlOwnerEmail.lower() == (self.email).lower() :
            return True
        else : 
            return False
    

    def delete(self):
        try:
            if self.__checkShortLinkOwner() : 
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM links WHERE shortLink = %s", (self.shortLink,))
                self.conn.commit()
                return True
            else : 
                return False
            
        except Exception as e:
            return False
        finally:
            self.conn.close()









class ShowUrlWithShortLink:
    def __init__(self, shortLink , byEmail = False):
        _DbCreator.createDB()
        self.shortLink = shortLink
        self.byEmail = byEmail

        self.conn = mysql.connect(host=HOST,
                                   user=DBUSERNAME,
                                     password=DBPASSWORD,
                                       database="links")
        
    def __finder(self) : 
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM links WHERE shortLink = %s", (self.shortLink,))
            result = cursor.fetchone()
            self.conn.close()
            return result if result else False
        except Exception as e:
            return False


    def show(self):
        if self.byEmail :
            return self.__finder()
        else : 
            try : 
                return self.__finder()[2]
            except Exception : 
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
