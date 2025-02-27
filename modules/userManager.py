from hashlib import sha256

import mysql.connector as mysql

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
        cursor.execute("CREATE DATABASE IF NOT EXISTS users")
        conn.close()






class AddUser : 
    def __init__(self , email , password) : 
        _DbCreator.createDB()

        self.email = email
        self.password = password
        self.username = email[:email.index("@")]



        self.conn = mysql.connect(host = HOST, 
                     user = DBUSERNAME , 
                     password = DBPASSWORD , 
                     database = "users")




    def __passHasher(self) : 
        return (sha256((self.password).encode('utf-8')).hexdigest())


    def __createTable(self) : 
        cursor = (self.conn).cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INT PRIMARY KEY AUTO_INCREMENT ,
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255)
            )
        """)
        


    def adduser(self) : 
        try : 
            self.__createTable()

            cursor = (self.conn).cursor()
            cursor.execute("INSERT INTO users(email , password)  VALUES(%s , %s)" , 
                        (self.email , self.__passHasher()))
            (self.conn).commit()
            (self.conn).close()

            mainPageMetric.Users().addToUsersCounter()

            return True
        except mysql.IntegrityError : 
            return [False , "userExists"]
        except Exception as e : 
            return [False , e]
        











class CheckUserValidation:
    def __init__(self, email, password):
        _DbCreator.createDB()
        self.email = email
        self.password = password


        self.conn = mysql.connect(host = HOST, 
                     user = DBUSERNAME , 
                     password = DBPASSWORD , 
                     database = "users")




    def __passHasher(self):
        return sha256(self.password.encode('utf-8')).hexdigest()

    def __userExistenceChecker(self):
        try : 
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute("""
                SELECT password FROM users 
                WHERE email=%s  
                ORDER BY id DESC LIMIT 1
            """, (self.email,))
            result = cursor.fetchone()
            conn.close()

            if result:  
                stored_password = result[0]
                return stored_password == self.__passHasher()
            return False
        
        except Exception : 
            return False
        
        finally : 
            conn.close()


    def validationChecker(self):
        return self.__userExistenceChecker()