
"""
User Management Module

This module is designed to manage users by providing functionalities such as:
- Adding new users
- Validating user credentials with passwords

It uses MySQL for data management with the following structure:

Database: users  
Table: users  
- id INT PRIMARY KEY AUTO_INCREMENT  
- email VARCHAR(255) UNIQUE (used as username)  
- password VARCHAR(255) (hashed using SHA-256 and encoded in UTF-8)  

All passwords are securely hashed using SHA-256 and stored as UTF-8 encoded strings.

Author: Mateo-rfz
Date: 2025-02-28  
License: GPL-3.0

Dependencies:
listed on requirements.txt (install with "pip install -r requirements.txt")
- mysql-connector-python
- hashlib

Usage:
    from user_module import add_user, validate_user

    #add new user with email and password
    userManager.AddUser("user@example.com", "password123").adduser()

    #check user validation with email and password
    userManager.CheckUserValidation("user@example.com", "password123").validationChecker()
"""



#use hash lib for hash passwords on database
from hashlib import sha256

import mysql.connector as mysql

from modules import mainPageMetric

#all database connection info on config.py
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