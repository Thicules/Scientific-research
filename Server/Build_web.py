from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from keras.models import load_model
import numpy as np
from PIL import Image
import geocoder 
from ISR.models import RDN, RRDN

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

@app.route('/')
def welcome():
    return render_template('index.html')

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

    # Lấy giá trị tọa độ từ dữ liệu POST
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    # Chuyển đổi tọa độ sang định dạng chuỗi với kí hiệu đông/tây, nam/bắc
    g = geocoder.google([latitude, longitude], method='reverse')
    location_str = g.address

    # Lưu tập tin ảnh vào thư mục static/images trên server
    filename = secure_filename(file.filename)
    file_path = os.path.join('static', 'images', filename)
    file.save(file_path)

    # Tăng độ phân giải ảnh
    sr_img = upscale_image(file_path)
    sr_img.save(file_path)

    # Chạy model và đổi tên tệp tin ảnh thành dạng filename_res_location
    res = animal(file_path)
    res_str = res.replace(' ', '_')
    new_filename = f'{os.path.splitext(filename)[0]}_{res_str}_{latitude},{longitude}{os.path.splitext(filename)[1]}'
    new_file_path = os.path.join('static', 'images', new_filename)
    os.rename(file_path, new_file_path)

    # Trả về kết quả và địa chỉ của địa điểm
    return res, location_str

@app.route('/all')
def show_all():
    images = []
    results = {}
    locations = {}
    for filename in os.listdir(os.path.join('static', 'images')):
        if allowed_file(filename):
            images.append(filename)
            res = os.path.splitext(filename)[0].split('_')[-2]
            results[filename] = res
            lat_long = os.path.splitext(filename)[0].split('_')[-1]
            if ',' in lat_long:
                lat, long = lat_long.split(',')
            else:
                lat = long = lat_long
            locations[filename] = {'lat': lat, 'long': long}

    return render_template('all.html', images=images, results=results, locations=locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
