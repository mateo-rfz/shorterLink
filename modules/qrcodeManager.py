import io
import qrcode
import redis


from modules import config





class CreateQrCode : 
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
                (self.conn).setex(self.url, 14400 , final)
            
            return self.url
        
        except Exception as e : 
            return e
        




class fetchQrCode : 
    def __init__(self , url : str) : 
        self.url = url.lower()
        self.conn = redis.Redis(config.REDISHOST , config.REDISPORT)

    def fetch(self) : 
        try : 
            if not (self.conn).exists(self.url) : 
                return False
            
            qr = (self.conn).get(self.url)
            return qr
        except Exception : 
            return False
        
        
        

    

