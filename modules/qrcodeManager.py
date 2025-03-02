"""
QR Code Manager Module

This module is designed to manage QR codes by providing functionalities such as:
- Creating a QR code for a given URL
- Fetching a QR code by its associated URL (name)

Database:
- Redis (KEY: url, VALUE: QR code)

Database Behavior:
- QR codes expire after 4 hours 
- The expiration time can be modified in modules/config.py

Author: Mateo-rfz
Date: 2025-03-02
License: GPL-3.0

Dependencies:
Listed in requirements.txt (install with "pip install -r requirements.txt")
- redis
- qrcode
- io

Usage:
    from modules import qrcodeManager

    # Create a new QR code
    qrcodeManager.CreateQrCode("https://example.com").create()

    # Fetch a QR code by URL
    qrcodeManager.fetchQrCode("https://example.com").fetch()
"""

#for create byte buffer on memory
import io

#for create qrcode
import qrcode

#for connect to redis database
import redis

#all database connection info on config.py
from modules import config






class CreateQrCode : 
    """
    CreateQrCode Class

    This class is responsible for generating QR codes and storing them in Redis.

    Redis structure:
    - KEY: URL (lowercase)
    - VALUE: QR code (binary data)

    Methods:
    - __init__(url: str): Initializes the Redis connection and sets the target URL.
    - create(): Generates a QR code for the given URL and stores it in Redis with an expiration time.
    """

    def __init__(self , url : str) : 
        self.url = url.lower()

        self.conn = redis.Redis(config.REDISHOST , config.REDISPORT)
    
    def create(self) : 
        try : 
            if (self.conn).exists(self.url) == 1 : 
                return self.url
                
            with io.BytesIO() as buffer:
                # create qrcode
                qr = qrcode.make(self.url)
                qr.save(buffer, format="PNG")

                # convert to bin
                final = buffer.getvalue()

                # save on redis
                (self.conn).setex(self.url, config.EXPIRETIME , final)
            
            return self.url
        
        except Exception as e : 
            return e
        








class FetchQrCode:
    """
    FetchQrCode Class

    This class is responsible for retrieving QR codes from Redis.

    Redis structure:
    - KEY: URL (lowercase)
    - VALUE: QR code (binary data)

    Methods:
    - __init__(url: str): Initializes the Redis connection and sets the target URL.
    - fetch(): Retrieves the QR code from Redis. Returns the QR code binary data if found, otherwise False.
    """
    def __init__(self, url: str):
        self.url = url.lower()
        self.conn = redis.Redis(config.REDISHOST, config.REDISPORT)

    def fetch(self):
        """
        Fetches the QR code from Redis.

        Returns:
            bytes: QR code binary data if found.
            bool: False if the QR code does not exist or an error occurs.
        """
        try:
            if not self.conn.exists(self.url):
                return False
            
            qr = self.conn.get(self.url)
            return qr
        except Exception:
            return False

        
        
