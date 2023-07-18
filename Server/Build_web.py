from flask import Flask, render_template, send_file, redirect, url_for, request, make_response
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from keras.models import load_model
import numpy as np
from keras.utils import image_utils
from PIL import Image


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

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image uploaded.', 400

    file = request.files['image']
    if file.filename == '':
        return 'No image selected.', 400
    if not allowed_file(file.filename):
        return 'Invalid file type.', 400

    # Lưu tập tin ảnh vào thư mục static/images trên server
    filename = secure_filename(file.filename)
    file_path = os.path.join('static', 'images', filename)
    file.save(file_path)

    # Chạy model và đổi tên tệp tin ảnh thành dạng filename:res
    res = animal(file_path)
    new_filename = f'{os.path.splitext(filename)[0]}_{res}{os.path.splitext(filename)[1]}'
    new_file_path = os.path.join('static', 'images', new_filename)
    os.rename(file_path, new_file_path)

    #Phản hồi kết quả
    return res

@app.route('/all')
def show_all():
    images = []
    results = {}
    for filename in os.listdir(os.path.join('static', 'images')):
        if allowed_file(filename):
            images.append(filename)
            res = os.path.splitext(filename)[0].split('_')[-1]
            results[filename] = res

    return render_template('all.html', images=images, results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)