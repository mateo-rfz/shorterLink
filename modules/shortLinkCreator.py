import random
import string
# from modules import dbController


def createShortLink() :
    while True : 
        all_chars = string.ascii_letters + string.digits

        final = ""

        p = random.choices(all_chars , k=5)
        for char in p : 
            final = final + char

        shLinks = dbController.allShortLinks()
        for i in shLinks : 
            if p == i : 
                break
        else : 
            return p




def createSpecialLink(suggestLink) : 
    pass

