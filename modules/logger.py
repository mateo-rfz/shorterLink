import datetime
import sqlite3


class Logger:
    def __init__(self, action: str, ip: str, email: str):
        self.action = action
        self.ip = ip
        self.email = email
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn = sqlite3.connect("log.db")

    def __createTable(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                ip TEXT,
                email TEXT,
                time TEXT
            )
        """)
        self.conn.commit()

    def logWriter(self) -> bool:
        try:
            self.__createTable()

            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO logs (action, ip, email, time)
                VALUES (?, ?, ?, ?)
            """, (self.action, self.ip, self.email, self.time))
            self.conn.commit()

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            self.conn.close()
