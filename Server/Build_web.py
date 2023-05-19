from flask import Flask, render_template, send_file, redirect, url_for, request
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from keras.models import load_model
import numpy as np
from keras.utils import image_utils
def animal():
    classifier = load_model('catdog_cnn_model.h5')
    pathtofile="C:/Users/Cao Thi/Desktop/Scientific-research/Server/images"
    # Get a list of all image files sorted by modification time
    image_files = sorted([os.path.join(pathtofile, f) for f in os.listdir(pathtofile) if f.endswith('.jpg')], key=os.path.getmtime, reverse=True)

    # Load the latest image file
    test_image =image_utils.load_img(image_files[0],target_size =(64,64,3))
    test_image =image_utils.img_to_array(test_image)
    test_image =np.expand_dims(test_image, axis =0)
    result = classifier.predict(test_image)
    if result[0][0] >= 0.5:
        prediction = 'dog'
    else:
        prediction = 'cat'
    return(prediction)


app = Flask(__name__)

@app.route('/')
def welcome():
    return redirect('/upload')

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'images'))
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Kiểm tra phần mở rộng của file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Tạo thư mục lưu trữ tệp tin nếu nó chưa tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Xử lý yêu cầu đăng ảnh lên máy chủ web
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    error = None
    if request.method == 'POST':
        # Kiểm tra xem request có chứa file hình ảnh hay không
        if 'file' not in request.files:
            return 'No file selected', 400

        file = request.files['file']

        # Kiểm tra xem file có hợp lệ hay không
        if file and allowed_file(file.filename):
            # Lưu file vào thư mục UPLOAD_FOLDER với tên gồm thời gian hiện tại và tên file gốc
            filename = secure_filename(file.filename)
            now = datetime.now().strftime("%Y%m%d-%H%M%S")
            new_filename = f"{now}-{filename}"
            file.save(os.path.join(UPLOAD_FOLDER, new_filename))
              # Run script test.py với đường dẫn đến tệp tin ảnh với đối số
            

            caption = animal() # Sử dụng dự đoán làm chú thích
            print(caption)
            return render_template('image.html', filename=new_filename, prediction=caption)

        else:
            return 'Invalid file format', 400
    return render_template('upload.html', error=error)


  
# Xử lý yêu cầu nhận ảnh từ máy chủ web
@app.route('/image/<filename>')
def get_image(filename):
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)
    except FileNotFoundError:
        return 'Error: File not found'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080, debug=True)
