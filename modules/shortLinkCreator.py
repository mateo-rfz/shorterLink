import random
import string
from modules import dbController


def createShortLink() :
    while True : 
        all_chars = string.ascii_letters + string.digits
        p1 = random.choice(all_chars)
        p2 = random.choice(all_chars)
        p3 = random.choice(all_chars)
        p4 = random.choice(all_chars)
        p5 = random.choice(all_chars)


        p = (p1 + p2 + p3 + p4 + p5)
 
        shLinks = dbController.allShortLinks()
        for i in shLinks : 
            if p == i : 
                break
        else : 
            return p
