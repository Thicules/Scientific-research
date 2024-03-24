import requests
import io
import os
import cv2
import time
import random

# Đường dẫn đến thư mục lưu trữ ảnh
image_dir = "C:\\Users\\BAO NGAN\\Downloads\\hi"

# Thông tin user
username = "baongandepgai"
password = "123456"

# Địa chỉ của server
server_url = 'http://127.0.0.1:8080/upload'

# Khởi tạo camera
camera = cv2.VideoCapture(0)

while True:
    # Đọc khung hình từ camera
    ret, frame = camera.read()

    # Tạo tên tệp tin ảnh dựa trên thời gian hiện tại
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}.jpg"
    image_path = os.path.join(image_dir, filename)

    # Lưu khung hình xuống thư mục lưu trữ
    cv2.imwrite(image_path, frame)

    # Sử dụng Google Maps Geocoding API để lấy tọa độ của máy chủ gửi lên
    latitude = random.uniform(-90,90)
    longitude = random.uniform(-180,180)

    # Chuẩn bị dữ liệu để gửi yêu cầu POST đến server
    with open(image_path, 'rb') as f:
        image_bytes = io.BytesIO(f.read())

    files = {'image': (filename, image_bytes, 'image/jpeg')}
    data = {'latitude': latitude, 'longitude': longitude, 'username': username, 'password': password}

    # Gửi yêu cầu POST đến server
    response = requests.post(server_url, files=files, data=data)

    # Chuyển đổi giá trị latitude sang độ và phút
    lat_degree = int(abs(latitude))
    lat_minute = (abs(latitude) - lat_degree) * 60
    lat_str = "{}°{:.6f}'".format(lat_degree, lat_minute) + "N" if latitude >= 0 else "{}° {:.6f}'".format(lat_degree,
                                                                                                           lat_minute) + "S"

    # Chuyển đổi giá trị longitude sang độ và phút
    long_degree = int(abs(longitude))
    long_minute = (abs(longitude) - long_degree) * 60
    long_str = "{}°{:.6f}'".format(long_degree, long_minute) + "E" if longitude >= 0 else "{}° {:.6f}'".format(
        long_degree, long_minute) + "W"

    # In kết quả trả về từ server và tọa độ với kí hiệu đông/tây, nam/bắc
    print(response.text, lat_str, long_str)

    # Chờ 5 giây trước khi chụp ảnh tiếp theo
    time.sleep(5)

camera.release()