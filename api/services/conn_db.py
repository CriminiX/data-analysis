import mysql.connector
import os


class DataBaseConn:

    def __init__(self):
        self.db_name = 'db_criminix'
        self.db_user = os.environ['db_user']
        self.db_pass = os.environ['db_pass']
        self.db_host = 'localhost'
        self.db_port = '3306'
        self.conn    = None

    def db_connect(self):
        self.conn = mysql.connector.connect(
            host     = self.db_host,
            port     = self.db_port,
            user     = self.db_user,
            password = self.db_pass,
            database = self.db_name
        )
        return self.conn.cursor()
    
    def db_disconnect(self):
        self.conn.close()
    
    