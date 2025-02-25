import random
import sqlite3
import string


class AddUrl:
    def __init__(self, email, originLink, shortLink=None):
        self.email = email
        self.originLink = originLink
        self.allchars = string.ascii_letters + string.digits

        if shortLink is None:
            self.shortLink = self.__createRandomShortLink()
        else:
            self.shortLink = shortLink if not self.__checkUrlExistence(shortLink) else False

    def __checkUrlExistence(self, targetUrl):
        self.__createTable()

        conn = sqlite3.connect("links.db")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM links WHERE shortLink = ?", (targetUrl,))
        result = cursor.fetchone()
        conn.close()
        return result is not None



    def __createRandomShortLink(self):
        while True:
            shortLink = "".join(random.choices(self.allchars, k=5))
            if not self.__checkUrlExistence(shortLink):
                return shortLink




    def __createTable(self):
        conn = sqlite3.connect("links.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS links(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                originLink TEXT,
                shortLink TEXT UNIQUE
            )
        """)
        conn.commit()
        conn.close()

    def __addToDb(self):
        self.__createTable()
        conn = sqlite3.connect("links.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO links (email, originLink, shortLink) 
            VALUES (?, ?, ?)
        """, (self.email, self.originLink, self.shortLink))
        conn.commit()
        conn.close()
        return True

    def add(self):
        if not self.shortLink:
            return False
        self.__addToDb()
        return self.shortLink















class DelUrl : 
    def __init__(self , shortLink) : 
        self.shortLink = shortLink 
    

    def delete(self) : 
        try : 
            conn = sqlite3.connect("links.db")
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM links
                WHERE shortLink =? ;
            """, (self.shortLink,))
            conn.commit()
            return True
        except Exception as e : 
            return [False , e]
        finally : 
            conn.close()