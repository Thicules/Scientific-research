from source import app
from flask import render_template, redirect, session,request
from source.models_mvc.user_model import User
from source import config

@app.route('/userHome',methods=['GET', 'POST'])
def userHome():
    return render_template('userHome.html')

@app.route('/userAbout')
def userAbout():
    return render_template('userAbout.html')

@app.route('/userContact')
def userContact():
    return render_template('userContact.html')

@app.route('/ava', methods=['POST'])
def upload():
    return redirect('/editProfile')

@app.route('/profile')
def profile():
    # Lấy danh sách đường dẫn hình ảnh từ cơ sở dữ liệu dựa trên người dùng hiện tại
    user_id = session['id']  # Lấy id người dùng từ session

    #gọi model
    results=User.getPathImg(user_id=user_id)

    # Lấy danh sách đường dẫn hình ảnh từ kết quả truy vấn
    image_paths = [result[0] for result in results]

    # Render mẫu 'profile.html' với danh sách đường dẫn hình ảnh
    return render_template('profile.html', image_paths=image_paths)

@app.route('/userPics')
def userPics():
    # Lấy danh sách đường dẫn hình ảnh và vị trí từ cơ sở dữ liệu dựa trên người dùng hiện tại
    user_id = session['id']  # Lấy id người dùng từ session

    #gọi model
    results= User.getImgInfo(user_id=user_id)

    # Lấy danh sách đường dẫn hình ảnh và vị trí từ kết quả truy vấn
    image_data = [{'path': result[0], 'position': result[1], 'result': result[2]} for result in results]

    # Render mẫu 'userPics.html' với danh sách đường dẫn hình ảnh và vị trí
    return render_template('userPics.html', image_data=image_data)

@app.route('/editProfile')
def editProfile():
    # Thực hiện truy vấn SQL để lấy thông tin người dùng từ cơ sở dữ liệu
    user_id = session['id']  # ID người dùng cần lấy thông tin

    #gọi model
    user_data=User.getUserInfo(user_id=user_id)

    # Trả về template HTML và truyền dữ liệu người dùng vào template
    return render_template('editProfile.html', user_data=user_data)

@app.route('/userAll')
def show_all():
    #Gọi model
    results=User.getAllImg()
    # Lấy danh sách đường dẫn hình ảnh và vị trí từ kết quả truy vấn
    image_all = [{'result': result[0], 'position': result[1], 'path': result[2]} for result in results]
    
    # Render mẫu 'userPics.html' với danh sách đường dẫn hình ảnh và vị trí
    return render_template('userAll.html', image_all=image_all)


@app.route('/update', methods=['POST'])
def update():
    if 'fileToUpload' not in request.files:
        return "No file uploaded"

    file = request.files['fileToUpload']
    if file.filename == '':
        return "No file selected"

    target_dir = 'static/images/avatar/'
    user_id = session.get('id')  # Lấy ID người dùng từ session

    target_file = target_dir + f"user_{user_id}.jpg"  # Đặt tên tệp hình ảnh với user_id

    if not config.allowed_file(file.filename):
        return 'Invalid file type.', 400

    file.save(target_file)
    
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
    #Gọi model ghi vào database
    User.editUserInfo(full_name,gender,phone,date_of_birth,street,city,state,email,user_id)
    return redirect('/profile')