
#___________________________________________________Mysql
HOST = "localhost"
DBUSERNAME = "root"
DBPASSWORD = "root"

#Default mysql port is 3306
DBPORT = 3306

#___________________________________________________REDIS

#REDIS
REDISHOST = "localhost"
REDISPORT = 6379
EXPIRETIME = 14400 #4h
"""
time table for expire qrcode on redis

1h -> 3600
2h -> 7200
3h -> 10800
4h -> 14400
5h -> 18000
6h -> 21600
"""