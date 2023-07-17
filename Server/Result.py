from flask import Flask, render_template, send_file, redirect, url_for 
import requests
from PIL import Image
import io
import os

# Đường dẫn đến file ảnh cần gửi lên server
image_path = 'E:/Scientific-research/Server/images/20230519-212816-OIP.jpg'

# Lấy tên tệp tin ảnh từ đường dẫn
filename = os.path.basename(image_path)

# Địa chỉ của server
server_url = 'http://127.0.0.1:8080/upload'

# Đọc ảnh và chuyển đổi sang định dạng bytes
with open(image_path, 'rb') as f:
    image_bytes = io.BytesIO(f.read())

# Chuẩn bị dữ liệu để gửi yêu cầu POST đến server
files = {'image': (filename, image_bytes, 'image/jpeg')}

# Gửi yêu cầu POST đến server
response = requests.post(server_url, files=files)

# In kết quả trả về từ server
print(response.text)