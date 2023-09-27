from source import app
from flask import request,session,render_template,redirect,url_for
from source.models_mvc.account_model import Account
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_caching import Cache
import random
import string

# Create random string for the verification link
def generate_random_string(length):
    characters = string.ascii_letters + string.digits 
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# Create the MIMEMultipart object
message = MIMEMultipart()
app.config['CACHE_TYPE'] = 'simple' 
cache = Cache(app)

# Send verification email
def send_verification_email(email, username):    
    smtp_host= 'smtp.gmail.com'
    smtp_port = 587
    smpt_username = 'cloudkeeper4@gmail.com'
    smtp_password = 'pygr pjpa cxht wgel'

    #Create MIMEMuiltipart object
    message= MIMEMultipart()
    message['From'] = smpt_username
    message['To'] = email
    message['Subject'] = 'Account Verification'

    # Generate the verification link using the username
    verification_link = url_for('verify', username=username, string=generate_random_string(50), _external=True)

    # Create the email message
    body = f'Hi {username},\n\nPlease click the following link to verify your account:\n{verification_link} \n\nRegard, \nRoad Damage Support team'
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smpt_username,smtp_password)
        server.sendmail(smpt_username, email, message.as_string())
        server.quit()
    except Exception as ex:
        print('Error sending verfication mail: ', str(ex))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account=Account.login(username,password)
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('userHome.html', msg = msg)
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            account=Account.checkExistence(username=username)
            if account:
                msg = 'Username already exists!'
                account=Account.checkExistenceEmail(email=email)
            elif account:
                msg = 'Email already exists!'
            else:                
                cache.set('user_info', {'username': username, 'password': password, 'email': email,})                
                send_verification_email(email, username)         
                msg = 'Please check your email to verify your account'                
                
    elif request.method == 'POST':
        msg = 'Please fill out the form!'    
    return render_template('login.html', msg=msg)

@app.route('/register/verify', methods=['GET'])
def verify():
    user_info = cache.get('user_info')   
    if user_info is not None: 
        username = user_info['username']
        password = user_info['password']
        email = user_info['email']
        Account.insertAccount(username, password, email)  
        cache.delete('user_info')      
        return render_template('register_successfully.html',)
    else: 
        return render_template("login.html")          
    
    