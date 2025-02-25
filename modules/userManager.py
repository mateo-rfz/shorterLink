from hashlib import sha256
import sqlite3




class AddUser : 
    def __init__(self , email , password) : 
        self.email = email
        self.password = password
        self.username = email[:email.index("@")]

    def __passHasher(self) : 
        return (sha256((self.password).encode('utf-8')).hexdigest())


    def __createTable(self) : 
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT
            )
        """)
        conn.close()


    def adduser(self) : 
        try : 
            self.__createTable()

            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users(email , password)  VALUES(? , ?)" , 
                        (self.email , self.__passHasher()))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError : 
            return [False , "userExists"]
        except Exception as e : 
            return [False , e]
        











class CheckUserValidation:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __passHasher(self):
        return sha256(self.password.encode('utf-8')).hexdigest()

    def __userExistenceChecker(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT password FROM users 
            WHERE email=? 
            ORDER BY id DESC LIMIT 1
        """, (self.email,))
        result = cursor.fetchone()
        conn.close()

        if result:  
            stored_password = result[0]
            return stored_password == self.__passHasher()
        return False


    def validationChecker(self):
        return self.__userExistenceChecker()