from flask import Flask, request, render_template, session, redirect, url_for
import socket, os, json
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from utils import *

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/testsql', methods=['GET', 'POST'])
def sqltest():
    if session.get('logged_in') == True:
        # Connect to the database
        connection = getMysqlConnection()
        cursor = connection.cursor()
        sql = "SELECT `password` FROM `User` WHERE `username`=%s"
        cursor.execute(sql, ('test123',))
        result = cursor.fetchone()
        if not result:
            sql = "INSERT INTO `User` (`username`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('test123', 'testing'))
            cursor.execute(sql, ('admin', 'gotcha'))
            connection.commit()
        sql = "SELECT `id`, `password` FROM `User` WHERE `username`=%s"
        cursor.execute(sql, ('test123',))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
    return render_template('test.html', result=result)

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        if request.form['Button'] == 'CreateUser':
            username = request.form['username']
            password = request.form['password']
            pw_hash = get_hash(password)
            if not ifExists(username):
                connection = getMysqlConnection()
                cursor = connection.cursor()
                sql = "INSERT INTO `User` (`username`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, (username, pw_hash))
                connection.commit()
                cursor.close()
                connection.close()
                output = "User " + username + " sucessfully added"
                return render_template('newuser.html', output=output)
            else:
                output = "User " + username + " already exists"
                return render_template('newuser.html', output=output)
        elif request.form['Button'] == 'BackToLogin':
            output = "Insert Valid Username and Password to Login"
            return render_template('login.html', output=output)
    output = "Start by Adding Credentials"
    return render_template('newuser.html', output=output)

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if session.get('logged_in') == True and session.get('username') != None:
        output = "Upload Files and Videos"
        p = str(app.config['UPLOAD_FOLDER']) + str(session.get('username')) #make user specific path in Videos
        if os.path.exists(p) != True:
            os.mkdir(p)                 #Create user specific dir for user if it doesnt already exist
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                output = "No file part"
                return render_template('index.html', output=output)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                output = "No selected file"
                return render_template('index.html', output=output)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(p, filename))                #p is path from above
                sql = "INSERT INTO `Videos` (`username`, `vidpath`) VALUES (%s, %s)"    #Add record of file upload to database
                cursor.execute(sql, (str(session.get('username')), p))
                output = "Successfully Uploaded File: " + filename
                return render_template('index.html', output=output)
        return render_template('index.html', output=output)
    else:
        return redirect(url_for('login'))

#CSFR TOKEN PYTHON: http://flask.pocoo.org/snippets/3/
@app.route('/login', methods=['GET', 'POST'])
def login():
    session['username'] = None
    if request.method == 'POST':
        if request.form['Button'] == 'Login':
            username  = request.form['username']
            password  = request.form['password']
            if not ifExists(username):
                output = "Username Supplied was invalid"
                return render_template('login.html', output=output)
            else:
                connection = getMysqlConnection()
                cursor = connection.cursor()
                sql = "SELECT `password` FROM `User` WHERE `username`=%s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                pw_hash = result[0]
                cursor.close()
                connection.close()
                if check_password(pw_hash, password):
                    session['username'] = username
                    session['logged_in'] = True
                    return redirect(url_for('mainpage'))
                else:
                    output = "Password Supplied was invalid"
                    return render_template('login.html', output=output)
        elif request.form['Button'] == 'CreateUser':
            return redirect(url_for('adduser'))
    output = "Insert Valid Username and Password to Login"
    return render_template('login.html', output=output)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)