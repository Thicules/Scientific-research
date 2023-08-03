from flask import Flask, render_template, send_file, redirect, url_for 
import requests
from PIL import Image
import io
import os
import googlemaps

# Đường dẫn đến file ảnh cần gửi lên server
image_path = "C:\\Users\\BAO NGAN\\Downloads\\8BWst4aF_400x400.jpg"

# Lấy tên tệp tin ảnh từ đường dẫn
filename = os.path.basename(image_path)

# Địa chỉ của server
server_url = 'http://127.0.0.1:8080/upload'

# Sử dụng Google Maps Geocoding API để lấy tọa độ của máy chủ gửi lên
gmaps = googlemaps.Client(key='AIzaSyCtQkhii_0MXu2paXoQyYLSd5DP2ERLtUs')
geocode_result = gmaps.geocode('me')
latitude = geocode_result[0]['geometry']['location']['lat']
longitude = geocode_result[0]['geometry']['location']['lng']

# Đọc ảnh và chuyển đổi sang định dạng bytes
with open(image_path, 'rb') as f:
    image_bytes = io.BytesIO(f.read())

# Chuẩn bị dữ liệu để gửi yêu cầu POST đến server
files = {'image': (filename, image_bytes, 'image/jpeg')}
data = {'latitude': latitude, 'longitude': longitude}

# Gửi yêu cầu POST đến server
response = requests.post(server_url, files=files, data=data)

# Chuyển đổi giá trị latitude sang độ và phút
lat_degree = int(abs(latitude))
lat_minute = (abs(latitude) - lat_degree) * 60
lat_str = "{}°{:.6f}'".format(lat_degree, lat_minute) + "N" if latitude >= 0 else "{}° {:.6f}'".format(lat_degree, lat_minute) + "S"

# Chuyển đổi giá trị longitude sang độ và phút
long_degree = int(abs(longitude))
long_minute = (abs(longitude) - long_degree) * 60
long_str = "{}°{:.6f}'".format(long_degree, long_minute) + "E" if longitude >= 0 else "{}° {:.6f}'".format(long_degree, long_minute) + "W"

# In kết quả trả về từ server và tọa độ với kí hiệu đông/tây, nam/bắc
print(response.text, lat_str, long_str)