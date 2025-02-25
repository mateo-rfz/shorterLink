import sqlite3





class LinkView : 
    def __init__(self , shortLink) : 
        self.shortLink = shortLink

    
    def view(self) : 
        try : 
            conn = sqlite3.connect("metrix.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM metrix 
                WHERE shortLink=? 
            """, (self.shortLink,))

            result = cursor.fetchone()
            return result
        except Exception : 
            return False
        




class AddView : 
    def __init__(self , shortLink) : 
        self.shortLink = shortLink


    def __createTable(self) : 
        conn = sqlite3.connect("metrix.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrix(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shortLink TEXT UNIQUE , 
                viewCounter INTEGER
            )
        """)
        conn.commit()
        conn.close()



    def addView(self) : 
        self.__createTable()
        try:
            conn = sqlite3.connect("metrix.db")
            cursor = conn.cursor()

    
            cursor.execute("""
                SELECT viewCounter FROM metrix WHERE shortLink=?
            """, (self.shortLink,))
            result = cursor.fetchone()

            if result:
                new_view = result[0] + 1
                cursor.execute("""
                    UPDATE metrix SET viewCounter=? WHERE shortLink=?
                """, (new_view, self.shortLink))
            else:
                cursor.execute("""
                    INSERT INTO metrix (shortLink, viewCounter) VALUES (?, ?)
                """, (self.shortLink, 1))

            conn.commit()
            return True
        except Exception as e:

            return [False, str(e)]
        
        finally:
            conn.close()






class AddItem : 
    def __init__(self , shortLink) : 
        self.shortLink = shortLink


    def __createTable(self) : 
        conn = sqlite3.connect("metrix.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrix(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shortLink TEXT UNIQUE , 
                viewCounter INTEGER
            )
        """)
        conn.commit()
        conn.close()


    def addItem(self) : 
        try : 
            self.__createTable()

            conn = sqlite3.connect("metrix.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO metrix(shortLink , viewCounter)  VALUES(? , ?)" , 
                        (self.shortLink , 0,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError : 
            return [False , "ItemExists"]
        except Exception as e : 
            return [False , e]


    