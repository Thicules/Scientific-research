from source import app
from flask import request
from werkzeug.utils import secure_filename
from source.models_mvc.account_model import Account
import geocoder
import os
from PIL import Image
from ISR.models import RDN, RRDN
from  model_train.load_model import ModelRoad
from source.models_mvc.user_model import User
from source import config
import numpy as np

def allowed_file(filename):
    ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    account=Account.validateAccount(username=username,password=password)
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
    file.save(os.path.join("source",file_path))

    # Tăng độ phân giải ảnh
    #sr_img = upscale_image(file_path)
    #sr_img.save(file_path)

    # Chạy model
    res = ModelRoad.predict(os.path.join('source',file_path))


    # Lưu thông tin ảnh vào cơ sở dữ liệu
    User.insertImg(account,filename,res,latitude,longitude,file_path)
    # Trả về kết quả và địa chỉ của địa điểm
    return res, location_str