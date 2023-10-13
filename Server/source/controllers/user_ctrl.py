from source import app
from flask import render_template, redirect, session,request, url_for
from source.models_mvc.user_model import User
from source import config
import os

@app.route('/userHome',methods=['GET', 'POST'])
def userHome():
    # Lấy danh sách đường dẫn hình ảnh từ cơ sở dữ liệu dựa trên người dùng hiện tại
    user_id = session['id']  # Lấy id người dùng từ session

    #gọi model
    user_data = User.getUserInfo(user_id=user_id)

    return render_template('userHome.html', user_data=user_data)

@app.route('/userAbout')
def userAbout():
    # Lấy danh sách đường dẫn hình ảnh từ cơ sở dữ liệu dựa trên người dùng hiện tại
    user_id = session['id']  # Lấy id người dùng từ session

    #gọi model
    user_data = User.getUserInfo(user_id=user_id)

    return render_template('userAbout.html', user_data=user_data)

@app.route('/userContact')
def userContact():
    # Lấy danh sách đường dẫn hình ảnh từ cơ sở dữ liệu dựa trên người dùng hiện tại
    user_id = session['id']  # Lấy id người dùng từ session

    #gọi model
    user_data = User.getUserInfo(user_id=user_id)

    return render_template('userContact.html', user_data=user_data)

@app.route('/ava', methods=['POST'])
def upload():
    return redirect('/editProfile')

@app.route('/profile')
def profile():
    # Lấy danh sách đường dẫn hình ảnh từ cơ sở dữ liệu dựa trên người dùng hiện tại
    user_id = session['id']  # Lấy id người dùng từ session

    #gọi model
    user_data = User.getUserInfo(user_id=user_id)
    results=User.getPathImg(user_id=user_id)

    # Lấy danh sách đường dẫn hình ảnh từ kết quả truy vấn
    image_paths = [result[0] for result in results]

    # Render mẫu 'profile.html' với danh sách đường dẫn hình ảnh
    return render_template('profile.html', image_paths=image_paths, user_data=user_data)

@app.route('/userPics')
def userPics():
    # Lấy danh sách đường dẫn hình ảnh và vị trí từ cơ sở dữ liệu dựa trên người dùng hiện tại
    user_id = session['id']  # Lấy id người dùng từ session

    #gọi model
    user_data = User.getUserInfo(user_id=user_id)
    results= User.getImgInfo(user_id=user_id)

    # Lấy danh sách đường dẫn hình ảnh và vị trí từ kết quả truy vấn
    image_data = [{'path': result[0], 'position': result[1], 'result': result[2], 'id':result[3]} for result in results]

    # Render mẫu 'userPics.html' với danh sách đường dẫn hình ảnh và vị trí
    return render_template('userPics.html', image_data=image_data, user_data=user_data)

@app.route('/editProfile', methods=['GET', 'POST'])
def editProfile():
    if request.method == 'POST':
        # Xác định ID người dùng từ session
        user_id = session['id']
        user_data = User.getUserInfo(user_id=user_id)

        # Khởi tạo giá trị mặc định cho ava
        ava = user_data['ava']

        # Kiểm tra và xử lý tải lên avatar
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                target_file = f"user_{user_id}.jpg"
                target_dir = os.path.join('static', 'images', 'avatar')
                ava_path = os.path.join(target_dir, target_file)
                file.save(os.path.join('source', ava_path))
                ava = ava_path

        # Lấy thông tin người dùng từ biểu mẫu HTML
        full_name = request.form.get('full_name')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        date_of_birth = request.form.get('date_of_birth')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        job = request.form.get('job')

        # Gọi model ghi vào database
        User.editUserInfo(full_name, gender, phone, date_of_birth, street, city, state, job, ava, user_id)

        # Điều hướng quay lại trang profile
        return redirect(url_for('profile'))
    else:
        # Xử lý khi yêu cầu là GET
        # Lấy thông tin người dùng từ cơ sở dữ liệu
        user_id = session['id']
        user_data = User.getUserInfo(user_id=user_id)

        # Trả về template HTML và truyền dữ liệu người dùng vào template
        return render_template('editProfile.html', user_data=user_data)
                           
@app.route('/userAll')
def show_all():
    # Lấy thông tin người dùng từ cơ sở dữ liệu
    user_id = session['id']

    #Gọi model
    results=User.getAllImg()
    user_data = User.getUserInfo(user_id=user_id)
    # Lấy danh sách đường dẫn hình ảnh và vị trí từ kết quả truy vấn
    image_all = [{'result': result[0], 'position': result[1], 'path': result[2]} for result in results]
    
    # Render mẫu 'userPics.html' với danh sách đường dẫn hình ảnh và vị trí
    return render_template('userAll.html', image_all=image_all, user_data=user_data)

#Cái này là post tọa độ mới
@app.route('/update_coordinates', methods=['POST'])
def update_coordinates():
    image_id = request.form['id']
    new_lat = request.form['lat']
    new_long = request.form['long']
    position=new_lat+','+new_long
    User.editPosition(image_id,position)

    # Gọi phương thức để cập nhật tọa độ vào cơ sở dữ liệu (ví dụ: User.updateImagePosition)
    # Thực hiện xác thực người dùng và kiểm tra quyền trước khi cập nhật

    # Trả về phản hồi (nếu cần)
    return redirect('/userPics')

@app.route('/delete_image', methods=['POST'])
def delete_image():
    image_id = request.form['id']
    User.deleteImage(image_id)
    # Thực hiện xác thực người dùng và kiểm tra quyền trước khi cập nhật

    # Trả về phản hồi (nếu cần)
    return redirect('/userPics')