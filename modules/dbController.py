import sqlite3


def createTable() : 
    conn = sqlite3.connect("links.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS links(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT, 
                       originLink TEXT , 
                       shortLink TEXT)""")




def createShortUrl(username , originLink , shortLink) : 
    createTable()
    conn = sqlite3.connect("links.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links(username , originLink , shortLink)  VALUES(? , ? , ?)" , (username , originLink , shortLink))
    conn.commit()
    
    return True





def urlFinder(shortLink) :
    createTable()
    conn = sqlite3.connect("links.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM links WHERE shortLink = ?" , (shortLink,))
    try : 
        return cursor.fetchall()[-1]
    except Exception : 
        return False




def allShortLinks() : 
    createTable()
    conn = sqlite3.connect("links.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM links")
    cursor = cursor.fetchall()

    final = []

    for i in cursor :  
        final.append(i[3])


    return final