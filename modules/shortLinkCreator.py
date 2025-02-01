import random
import string
from modules import dbController



class LinkManager : 
    """
    
    """
    def __init__(self) : 
        self.allShortLinks = dbController.allShortLinks() #all short links in data base
        self.allChars = string.ascii_letters + string.digits


    def createShortLink() :
        """
        
        """
        while True : 

            final = ""

            p = random.choices(self.allChars , k=5)
            for char in p : 
                final = final + char

            for i in self.allShortLinks : 
                if p == i : 
                    break
            else : 
                return p


    def createSpecialLink(suggestLink) :
        """
        
        """ 
        for i in self.allShortLinks : 
            if suggestLink == i : 
                #check for exists suggest url in data base
                return False

        return True







