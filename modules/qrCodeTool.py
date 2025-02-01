import qrcode
import os
import sys


class Qrcode : 
    def __init__(self , originUrl , shortUrl , path = "/tmp/qrcode") : 
        self.originUrl = originUrl
        self.shortUrl = shortUrl
        self.path = path


    def __checkFolderexists(self):
        os.makedirs(self.path, exist_ok=True) 

    
    def qrGenerator(self) : 
        self.__checkFolderexists()

        img = qrcode.make(self.originUrl)
        img.save(f"/tmp/qrcode/{self.shortUrl}.png")

        return True

