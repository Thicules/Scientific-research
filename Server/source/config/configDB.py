from flask_mysqldb import MySQLdb

class DB:
    conn = None
    DBNAME = "weblogin"
    DBIP = "localhost"
    DBUSER = "root"
    DBPASS = "baongan"
    def __init__(self):
        self.conn = MySQLdb.connect(self.DBIP,self.DBUSER,self.DBPASS,self.DBNAME)

    def cursor(self,cursorType=None):
        try:
            return self.conn.cursor(cursorType)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            return self.conn.cursor()