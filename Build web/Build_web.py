from flask import Flask, render_template, send_file, redirect, url_for, request
import os
from werkzeug.utils import secure_filename

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
            # Lưu file vào thư mục UPLOAD_FOLDER
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return 'ok', 200
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