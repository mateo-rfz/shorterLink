
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
    from modules import userManager

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

import string



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
        cursor.execute("CREATE DATABASE IF NOT EXISTS users")
        conn.close()






class AddUser : 
    """
    AddUser Class

    This class is used to add a new user to the database using email and password.  
    * Passwords are securely hashed(SHA-256) before being stored in the database.  

    methods : 
    - __passHasher : use for hash passwords
    - __createTable : use for create 'users' table in Mysql (IF NOT EXISTS)
    - __passwordSecurityChecker : use for check security off password (lenght + use digits + use letters)
    - adduser is main method in AddUser class for add user
    """
    def __init__(self , email , password) : 
        _DbCreator.createDB()

        self.email = email
        self.password = password



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
                password VARCHAR(300)
            )
        """)


    def __passwordSecurityChecker(self , passwd : str) : 
        passwd = passwd.replace(" " , "")
        if len(passwd) < 5 : 
            return "WEAKPASS"
        
        numChecker = False
        letterChecker = False

        digits = (string.digits).replace("" , " ").split()
        letters = (string.ascii_letters).replace("" , " ").split()

        for char in passwd : 
            if char in digits : 
                numChecker = True
            elif char in letters : 
                letterChecker = True

        if letterChecker and numChecker :
            return True
        else : 
            return "WEAKPASS"
        


    def adduser(self) : 
        try : 

            self.__createTable()
            


            cursor = (self.conn).cursor()
            cursor.execute("INSERT INTO users(email , password)  VALUES(%s , %s)" , 
                        (self.email , self.__passHasher()))
            

            """
            we add this checker after INSERT on database
            and before commit data on data base
            for check email exists with database and if exists rais error 
            else check security of password and if security of password is ok 
            commit the data
            """
            
            if self.__passwordSecurityChecker(self.password) == "WEAKPASS": 
                return "WEAKPASS"
            
            (self.conn).commit()
            (self.conn).close()

            mainPageMetric.Users().addToUsersCounter()

            return 300
        except mysql.IntegrityError : 
            return False
        except Exception as e : 
            False
        











class CheckUserValidation:
    """
    CheckUserValidation class

    This class is used to validate a user's credentials using email and password.

    Methods : 
    - __passHasher : use for hash passwords
    - __userExistenceChecker : this method use for check use existence and if exists check db password with input password
    - validationChecker : the main method in CheckUserValidation class this method return the final __userExistenceChecker answer
    """
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
                #We use a filter to search the database and return only the email.
                #and the resault[0] is only email
                return stored_password == self.__passHasher()
            return False
        
        except Exception : 
            return False
        
        finally : 
            conn.close()


    def validationChecker(self):
        return self.__userExistenceChecker()
    















class ChangeUserPassword : 
    def __init__(self , email : str , oldPassword : str , newPassword : str) -> bool : 
        self.email = email 
        self.oldPassword = oldPassword
        self.newPassword = newPassword
        self.hashNewPassword = self.__passHasher()



        self.conn = mysql.connect(host = HOST, 
                     user = DBUSERNAME , 
                     password = DBPASSWORD , 
                     database = "users")
        

    def __passHasher(self) : 
        return (sha256((self.newPassword).encode('utf-8')).hexdigest())
    


    def __passwordSecurityChecker(self , passwd : str) : 
        passwd = passwd.replace(" " , "")
        if len(passwd) < 5 : 
            return "WEAKPASS"
        
        numChecker = False
        letterChecker = False

        digits = (string.digits).replace("" , " ").split()
        letters = (string.ascii_letters).replace("" , " ").split()

        for char in passwd : 
            if char in digits : 
                numChecker = True
            elif char in letters : 
                letterChecker = True

        if letterChecker and numChecker :
            return True
        else : 
            return "WEAKPASS"
        


    
    def __checkValidation(self) : 
        try : 
            o = CheckUserValidation(self.email , self.oldPassword).validationChecker()

            if self.__passwordSecurityChecker(self.newPassword) == "WEAKPASS": 
                return "WEAKPASS"
            
            if o : 
                cursor = (self.conn).cursor()
                cursor.execute("""UPDATE users SET password = %s WHERE email = %s""" , (self.hashNewPassword , self.email,))
                (self.conn).commit()
            else :
                return False

            return True
        
        except Exception  as e: 
            return e
        
        finally : 
            (self.conn).close()
        


    def changePass(self) : 
        return self.__checkValidation()

            