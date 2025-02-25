from hashlib import sha256
import random
import string
import sqlite3


class AddRegisterKey:
    def __init__(self, email):
        self.email = email
        self.characters = string.ascii_letters + string.digits
        self.raw_key = ''.join(random.choices(self.characters, k=10)) 
        self.key = self.__passHasher(self.raw_key)

    def __passHasher(self, chars):
        return sha256(chars.encode('utf-8')).hexdigest()
    

    def __createTable(self) : 
        conn = sqlite3.connect("registerkeys.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keys(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                key TEXT
            )
        """)
        conn.close()

    
    def __checkKeyExistence(self) : 
        conn = sqlite3.connect("registerkeys.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM keys 
            WHERE email=? 
            ORDER BY id DESC LIMIT 1
        """, (self.email,))
        result = cursor.fetchone()
        conn.close()

        if result:  
            return True
        return False
    



    def __updateTheLastKey(self) : 
        try : 
            conn = sqlite3.connect("registerkeys.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE keys
                SET key=?
                WHERE email=?;
            """, (self.key , self.email,))
            conn.commit()
            conn.close()
            return True
        except Exception as e : 
            return [False , e]




    def __setKey(self) : 
        try : 
            self.__createTable()

            conn = sqlite3.connect("registerkeys.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO keys(email , key)  VALUES(? , ?)" , 
                        (self.email , self.key))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError : 
            return [False , "keyExists"]
        except Exception as e : 
            return [False , e]




    def registerKey(self):
        self.__createTable()
    
        if self.__checkKeyExistence() : 
            self.__updateTheLastKey()
            return self.key
        else : 
            self.__setKey()
            return self.key
        
















class KeyValidation : 
    def __init__(self , email , key) : 
        self.email = email 
        self.key = key


    def checkValidation(self) : 
        try : 
            conn = sqlite3.connect("registerkeys.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM keys 
                WHERE email=? 
                ORDER BY id DESC LIMIT 1
            """, (self.email,))
            result = cursor.fetchone()
            conn.close()

            if result[2] == self.key:  
                return True
            return False
        except Exception as e: 
            return [False , e]