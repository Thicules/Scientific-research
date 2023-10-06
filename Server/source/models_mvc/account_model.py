from flask_mysqldb import MySQL
import MySQLdb.cursors
from source import app
from source.config.configDB import DB 


class Account:
    # Xác thực tài khoản
    @staticmethod
    def validateAccount(username,password):
        db =DB()
        cursor=db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        cursor.close()
        return account
    
    #Đăng nhập
    @staticmethod
    def login(username,password):
        db = DB()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        cursor.close()
        return account
    
    #Kiếm tra sự tồn tại của tài khoản
    @staticmethod
    def checkExistence(username):
        db = DB()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        cursor.close()
        return account
    
    #Kiếm tra sự tồn tại của email
    @staticmethod
    def checkExistenceEmail(email):
        db = DB()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', (email,))
        account = cursor.fetchone()
        cursor.close()
        return account
    
    #Thêm tài khoản
    @staticmethod
    def insertAccount(username,password,email):
        db = DB()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        db.conn.commit()
        cursor.close()

    #Thay đổi mật khẩu người dùng
    @staticmethod
    def updatePassword(email, new_password):
        db = DB()
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE accounts SET password = %s WHERE email = %s', (new_password, email))
        db.conn.commit()
        cursor.close()