"""
Register Key Manager modules

This module is designed to manage register keys by providing functionalities such as:
- Add a new register key associated with an email
- Validate a register key for a given email

Database:
- MySQL (Database: rKeys, Table: users)

It links MySQL for data management with the following structure:

Database: rKeys  
Table: users  
Columns:  
 - id (INT, PRIMARY KEY, AUTO_INCREMENT)  
 - email (VARCHAR(255), UNIQUE)  
 - rk (VARCHAR(400)) — Register key

Author: Mateo-rfz  
Date: 2025-02-28  
License: GPL-3.0

Dependencies:  
listed on requirements.txt (install with "pip install -r requirements.txt")  
- mysql-connector-python  
- random  
- string  
- hashlib

Usage:
    from modules import registerKeyManager

    # Add a new register key associated with an email
    registerKeyManager.AddRegisterKey(email).registerKey()

    # Validate a register key for a given email
    registerKeyManager.KeyValidation(email, registerKey).checkValidation()
"""



from hashlib import sha256
import random
import string
# this modules use for create random register key

import mysql.connector as mysql

#all database connection info on config.py
from modules import config




HOST = config.HOST
DBUSERNAME = config.DBUSERNAME
DBPASSWORD = config.DBPASSWORD
DBPORT = config.DBPORT






class _DbCreator: 
    def createDB(self): 
        conn = mysql.connect(
            host=HOST, 
            user=DBUSERNAME, 
            password=DBPASSWORD 
        )

        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS rKeys")
        conn.close()







class AddRegisterKey:
    def __init__(self, email):
        _DbCreator().createDB()
        self.email = email
        self.characters = string.ascii_letters + string.digits
        self.raw_key = ''.join(random.choices(self.characters, k=10))
        self.key = self.__passHasher(self.raw_key)

        self.conn = mysql.connect(
            host=HOST,
            user=DBUSERNAME,
            password=DBPASSWORD,
            database="rKeys"
        )





    def __passHasher(self, chars):
        return sha256(chars.encode('utf-8')).hexdigest()






    def __createTable(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rKeys(
                id INT PRIMARY KEY AUTO_INCREMENT,
                email VARCHAR(255) UNIQUE,
                rk VARCHAR(400)
            )
        """)
        self.conn.commit()






    def __checkKeyExistence(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM rKeys 
            WHERE email = %s
            ORDER BY id DESC LIMIT 1
        """, (self.email,))
        return cursor.fetchone() is not None






    def __updateTheLastKey(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE rKeys
                SET rk = %s
                WHERE email = %s
            """, (self.key, self.email))
            self.conn.commit()
            return True
        except Exception:
            return False






    def __setKey(self):
        try:
            self.__createTable()
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO rKeys (email, rk) 
                VALUES (%s, %s)
            """, (self.email, self.key))
            self.conn.commit()
            return True
        except mysql.IntegrityError:
            return False
        except Exception:
            return False





    def registerKey(self):
        self.__createTable()
        if self.__checkKeyExistence():
            self.__updateTheLastKey()
        else:
            self.__setKey()
        return self.key







class KeyValidation:
    def __init__(self, email, key):
        _DbCreator().createDB()
        self.email = email
        self.key = key




        self.conn = mysql.connect(
            host=HOST,
            user=DBUSERNAME,
            password=DBPASSWORD,
            database="rKeys"
        )





    def checkValidation(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT rk FROM rKeys 
                WHERE email = %s
                ORDER BY id DESC LIMIT 1
            """, (self.email,))
            result = cursor.fetchone()
            self.conn.close()
            return result and result[0] == self.key
        except Exception:
            return False
