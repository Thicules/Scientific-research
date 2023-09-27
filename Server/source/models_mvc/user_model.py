from flask_mysqldb import MySQL
import MySQLdb.cursors
from source import app
from datetime import datetime
from source.config.configDB import DB


class User:
    @staticmethod
    def getUserInfo(user_id):
        db=DB()
        cur=db.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT * FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        user_data = cur.fetchone()
        cur.close()
        return user_data
    
    @staticmethod
    def getPathImg(user_id):
        db=DB()
        cur=db.cursor()
        query = "SELECT path FROM images WHERE user_id = %s"
        cur.execute(query, (user_id,))
        results = cur.fetchall()
        cur.close()
        return results
    
    @staticmethod
    def getImgInfo(user_id):
        db=DB()
        cur=db.cursor()
        query = "SELECT path, position, result FROM images WHERE user_id = %s"
        cur.execute(query, (user_id,))
        results = cur.fetchall()
        cur.close()
        return results
    
    @staticmethod
    def insertImg(account,filename,res,latitude,longitude,file_path):
        db=DB()
        cursor=db.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO images (user_id, namepics, result, position, upload_date, path) VALUES (%s, %s, %s, %s, %s, %s)",
                (account['id'], filename, res, f"{latitude},{longitude}", datetime.now().date(), file_path))
        db.conn.commit()
        cursor.close()

    @staticmethod
    def editUserInfo(full_name,gender,phone,date_of_birth,street,city,state,email,user_id):
        db=DB()
        cur=db.cursor()
        query = "UPDATE users SET full_name = %s, gender = %s, phone = %s, date_of_birth = %s, street = %s, city = %s, state = %s, email = %s WHERE id = %s"
        cur.execute(query, (full_name, gender, phone, date_of_birth, street, city, state, email, user_id))
        db.conn.commit()
        cur.close()
    
    @staticmethod
    def getAllImg(): 
        db=DB()
        cursor=db.cursor()
		# Truy vấn dữ liệu từ cơ sở dữ liệu
        cursor.execute("SELECT result, position, path FROM images")
        results = cursor.fetchall()
        cursor.close()
        return results
    
    