import qrcode
import os
import sys


class QrcodeTool : 
    def __init__(self , domain , shortUrl , path = "/tmp/qrcode") : 
        self.shortUrl = shortUrl
        self.domain = domain
        self.path = path


    def __checkFolderexists(self):
        os.makedirs(self.path, exist_ok=True) 

    
    def qrGenerator(self) : 
        self.__checkFolderexists()

        img = qrcode.make(self.domain + self.shortUrl)
        img.save(f"{self.path}/{self.shortUrl}.png")

        return True

