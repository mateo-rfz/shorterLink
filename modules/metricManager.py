from modules import config
import mysql.connector as mysql


HOST = config.HOST
DBUSERNAME = config.DBUSERNAME
DBPASSWORD = config.DBPASSWORD
DBPORT = config.DBPORT
DBNAME = "metrix"





class _DbCreator : 
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
