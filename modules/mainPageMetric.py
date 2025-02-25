import sqlite3


class Database:
    def __init__(self, db_name="mainPmetrix.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)


class LinksCounter:
    def __init__(self):
        self.db = Database()
        self.__createTable()

    def __createTable(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS linksCounter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                count INTEGER DEFAULT 0
            )
        """)
        cursor.execute("INSERT INTO linksCounter (count) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM linksCounter)")
        conn.commit()
        conn.close()

    def addToLinkCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE linksCounter SET count = count + 1")
        conn.commit()
        conn.close()

    def showLinksCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM linksCounter")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0







class Views:
    def __init__(self):
        self.db = Database()
        self.__createTable()

    def __createTable(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS viewsCounter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                count INTEGER DEFAULT 0
            )
        """)
        cursor.execute("INSERT INTO viewsCounter (count) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM viewsCounter)")
        conn.commit()
        conn.close()

    def addToViewsCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE viewsCounter SET count = count + 1")
        conn.commit()
        conn.close()

    def showViewsCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM viewsCounter")
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                count INTEGER DEFAULT 0
            )
        """)
        cursor.execute("INSERT INTO usersCounter (count) SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM usersCounter)")
        conn.commit()
        conn.close()

    def addToUsersCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE usersCounter SET count = count + 1")
        conn.commit()
        conn.close()

    def showUsersCounter(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM usersCounter")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

