from source import app
from flask import render_template, redirect, session,request, url_for
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

@app.route('/editProfile', methods=['GET', 'POST'])
def editProfile():
    if request.method == 'POST':
        # Xác định ID người dùng từ session
        user_id = session['id']

        # Lấy thông tin người dùng từ biểu mẫu HTML
        full_name = request.form.get('fullName')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        date_of_birth = request.form.get('date')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        job = request.form.get('job')
        print(request.form)

        # Khởi tạo giá trị mặc định cho target_file
        target_file = None

        # Kiểm tra và xử lý tải lên avatar
        if 'fileToUpload' in request.files:
            file = request.files['fileToUpload']
            if file.filename != '':
                target_dir = 'source/static/images/avatar/'
                # Đặt tên tệp hình ảnh với user_id
                target_file = target_dir + f"user_{user_id}.jpg"
                file.save(target_file)
        
        ava = target_file
        
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
    #Gọi model
    results=User.getAllImg()
    # Lấy danh sách đường dẫn hình ảnh và vị trí từ kết quả truy vấn
    image_all = [{'result': result[0], 'position': result[1], 'path': result[2]} for result in results]
    
    # Render mẫu 'userPics.html' với danh sách đường dẫn hình ảnh và vị trí
    return render_template('userAll.html', image_all=image_all)