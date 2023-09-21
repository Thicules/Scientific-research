from flask import Flask, render_template, redirect, url_for, session, request
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from keras.models import load_model
import numpy as np
from PIL import Image
import geocoder 
from ISR.models import RDN, RRDN
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

def animal(imagePath):
    classifier = load_model('catdog_cnn_model.h5')
    # Get a list of all image files sorted by modification time
    image_files = imagePath

    # Load the latest image file
    test_image = Image.open(image_files).resize((64, 64))   
    test_image = np.array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = classifier.predict(test_image)
    if result[0][0] >= 0.5:
        prediction = 'dog'
    else:
        prediction = 'cat'
    return prediction


app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY') or 'default secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'weblogin'
 
mysql = MySQL(app)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('userHome.html', msg = msg)
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, email, password, ))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('login.html', msg = msg)
 
# Xử lý yêu cầu đăng ảnh lên máy chủ web
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Hàm tăng độ phân giải ảnh
def upscale_image(image_path):
    # Đọc ảnh
    img = Image.open(image_path)
    # Chuẩn bị model tăng độ phân giải (SRGAN)
    rrdn = RRDN(weights='gans')

    # Tiến hành tăng độ phân giải
    sr_img = rrdn.predict(np.array(img))

    # Chuyển đổi ảnh numpy array sang định dạng Pillow Image
    sr_img = Image.fromarray(sr_img)

    return sr_img

@app.route('/home',methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/userHome',methods=['GET', 'POST'])
def userHome():
    return render_template('userHome.html')

@app.route('/userAbout')
def userAbout():
    return render_template('userAbout.html')

@app.route('/userContact')
def userContact():
    return render_template('userContact.html')

@app.route('/userPics')
def userPics():
    # Lấy danh sách đường dẫn hình ảnh và vị trí từ cơ sở dữ liệu dựa trên người dùng hiện tại
    user_id = session['id']  # Lấy id người dùng từ session
    cur = mysql.connection.cursor()
    query = "SELECT path, position, result FROM images WHERE user_id = %s"
    cur.execute(query, (user_id,))
    results = cur.fetchall()
    cur.close()

    # Lấy danh sách đường dẫn hình ảnh và vị trí từ kết quả truy vấn
    image_data = [{'path': result[0], 'position': result[1], 'result': result[2]} for result in results]

    # Render mẫu 'userPics.html' với danh sách đường dẫn hình ảnh và vị trí
    return render_template('userPics.html', image_data=image_data)

@app.route('/profile')
def profile():
    # Lấy danh sách đường dẫn hình ảnh từ cơ sở dữ liệu dựa trên người dùng hiện tại
    user_id = session['id']  # Lấy id người dùng từ session
    cur = mysql.connection.cursor()
    query = "SELECT path FROM images WHERE user_id = %s"
    cur.execute(query, (user_id,))
    results = cur.fetchall()
    cur.close()

    # Lấy danh sách đường dẫn hình ảnh từ kết quả truy vấn
    image_paths = [result[0] for result in results]

    # Render mẫu 'profile.html' với danh sách đường dẫn hình ảnh
    return render_template('profile.html', image_paths=image_paths)

@app.route('/editProfile')
def editProfile():
    # Thực hiện truy vấn SQL để lấy thông tin người dùng từ cơ sở dữ liệu
    user_id = session['id']  # ID người dùng cần lấy thông tin
    cur = mysql.connection.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    cur.execute(query, (user_id,))
    user_data = cur.fetchone()

    # Trả về template HTML và truyền dữ liệu người dùng vào template
    return render_template('editProfile.html', user_data=user_data)

@app.route('/ava', methods=['POST'])
def upload():
    if 'fileToUpload' not in request.files:
        return "No file uploaded"

    file = request.files['fileToUpload']
    if file.filename == '':
        return "No file selected"

    target_dir = 'static/images/avatar/'
    target_file = target_dir + file.filename
    allowed_extensions = {'jpg', 'jpeg', 'png'}

    if file.filename.split('.')[-1].lower() not in allowed_extensions:
        return "Invalid image format. Only JPG, JPEG, and PNG files are allowed."

    file.save(target_file)
    return redirect('/editProfile')

@app.route('/update', methods=['POST'])
def update():
    # Nhận dữ liệu từ biểu mẫu HTML và cập nhật thông tin người dùng vào cơ sở dữ liệu
    full_name = request.form['fullName']
    gender = request.form['gender']
    phone = request.form['phone']
    date_of_birth = request.form['date']
    street = request.form['Street']
    city = request.form['ciTy']
    state = request.form['sTate']
    email = request.form['email']
    
    # Thực hiện truy vấn SQL để cập nhật thông tin người dùng vào cơ sở dữ liệu
    user_id = session['id']  # ID người dùng cần lấy thông tin
    query = "UPDATE users SET full_name = %s, gender = %s, phone = %s, date_of_birth = %s, street = %s, city = %s, state = %s, email = %s WHERE id = %s"
    cur = mysql.connection.cursor()
    cur.execute(query, (full_name, gender, phone, date_of_birth, street, city, state, email, user_id))
    mysql.connection.commit()
    return redirect('/profile')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image uploaded.', 400

    file = request.files['image']
    if file.filename == '':
        return 'No image selected.', 400
    if not allowed_file(file.filename):
        return 'Invalid file type.', 400

    # Kiểm tra các giá trị latitude và longitude có tồn tại trong request.form
    if 'latitude' not in request.form or 'longitude' not in request.form:
        return 'Missing latitude or longitude values.', 400

    # Kiểm tra thông tin tài khoản
    if 'username' not in request.form or 'password' not in request.form:
        return 'Missing username or password.', 400

    username = request.form['username']
    password = request.form['password']

    # Xác thực thông tin tài khoản với cơ sở dữ liệu
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
    account = cursor.fetchone()
    if not account:
        return 'Invalid username or password.', 401
                
    # Lấy giá trị tọa độ từ dữ liệu POST
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    # Chuyển đổi tọa độ sang định dạng chuỗi với kí hiệu đông/tây, nam/bắc
    g = geocoder.google([latitude, longitude], method='reverse')
    location_str = g.address

    # Lưu tập tin ảnh vào thư mục static/images trên server
    filename = secure_filename(file.filename)
    file_path = os.path.join('static', 'images', 'road', filename)
    file.save(file_path)

    # Tăng độ phân giải ảnh
    sr_img = upscale_image(file_path)
    sr_img.save(file_path)

    # Chạy model
    res = animal(file_path)

    # Lưu thông tin ảnh vào cơ sở dữ liệu
    cursor.execute("INSERT INTO images (user_id, namepics, result, position, upload_date, path) VALUES (%s, %s, %s, %s, %s, %s)",
                (account['id'], filename, res, f"{latitude},{longitude}", datetime.now().date(), file_path))
    mysql.connection.commit()

    # Trả về kết quả và địa chỉ của địa điểm
    return res, location_str

@app.route('/userAll')
def show_all():

    cursor = mysql.connection.cursor()

    # Truy vấn dữ liệu từ cơ sở dữ liệu
    cursor.execute("SELECT result, position, path FROM images")
    results = cursor.fetchall()
    cursor.close()

    # Lấy danh sách đường dẫn hình ảnh và vị trí từ kết quả truy vấn
    image_all = [{'result': result[0], 'position': result[1], 'path': result[2]} for result in results]
    
    # Render mẫu 'userPics.html' với danh sách đường dẫn hình ảnh và vị trí
    return render_template('userAll.html', image_all=image_all)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)