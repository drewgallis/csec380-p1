from flask import Flask, request, render_template, session, redirect, url_for
import socket, os, json
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename

from utils import *

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['UPLOAD_FOLDER'] = "/etc/Videos"
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
        if request.method == 'POST':
            userid = int(get_userid(session.get('username')))
            file_name = request.form['filename']
            output = " Please Insert a Valid Filename"
            if request.form['Type'] == 'uploadfile' and file_name:
                p = str(app.config['UPLOAD_FOLDER']) + '/' + str(session.get('username')) #make user specific path in Videos
                if os.path.exists(p) != True:
                    os.mkdir(p)                 #Create user specific dir for user if it doesnt already exist
                    # check if the post request has the file part
                if 'file' not in request.files:
                    output = "No file part"
                    return render_template('index.html', output=output)
                file = request.files['file']
                if file.filename == '':
                    output = "No selected file"
                    return render_template('index.html', output=output)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(p, filename))                #p is path from above
                    timestamp = get_timestamp()
                    sql = "INSERT INTO `VideoStats` (`id`,`username`, `url`, `video_name`,`time_stamp`) VALUES (%s, %s, %s, %s, %s)"    #Add record of file upload to database
                    connection = getMysqlConnection()
                    cursor = connection.cursor()
                    cursor.execute(sql, (userid, str(session.get('username')), filename, file_name, timestamp))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    output = "Successfully Uploaded File: " + filename
                    return render_template('index.html', output=output)
            if request.form['Type'] == 'uploadurl' and file_name:
                p = str(app.config['UPLOAD_FOLDER']) + '/' + str(session.get('username')) #make user specific path in Videos
                if os.path.exists(p) != True:
                    os.mkdir(p)                 #Create user specific dir for user if it doesnt already exist
                    if 'url'not in request.form:
                        output = "No file part"
                        return render_template('index.html', output=output)
                url = request.form['url']
                filename = None
                if url != '':
                    if url.find('/'):
    	                filename = url.rsplit('/', 1)[1]
                    if url == '' or filename is None:
                        output = "No URL inputted or incorrect format"
                        return render_template('index.html', output=output)
                    if url and allowed_file(url):
                        filename = secure_filename(filename)
                        path = os.path.join(p, filename)
                        timestamp = get_timestamp()
                        sql = "INSERT INTO `VideoStats` (`id`,`username`, `url`, `video_name`,`time_stamp`) VALUES (%s, %s, %s, %s, %s)"    #Add record of file upload to database
                        connection = getMysqlConnection()
                        cursor = connection.cursor()
                        cursor.execute(sql, (userid, str(session.get('username')), filename, file_name, timestamp))
                        connection.commit()
                        cursor.close()
                        connection.close()
                        if download_url(url, path):
                            output = "Successfully uploaded url: " + filename
                            return render_template('index.html', output=output)
                        output = "Could not upload url: " + filename
                        return render_template('index.html', output=output)
                    else:
                        return render_template('index.html', output='Content not supported')
                else:
                    return render_template('index.html', output='Please insert a URL')
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

# still need to implement
@app.route('/search')
def search():
    if session.get('logged_in') == True and session.get('username') != None:
        result = get_users()
        return render_template('test.html', result=result)

# still need to implement
@app.route('/logout')
def logout():
    if session.get('logged_in') == True and session.get('username') != None:
        session.pop('username', None)
        return redirect(url_for('login'))

@app.route('/sql_classic', methods=['GET', 'POST'])
def sql_classic():
    if session.get('logged_in') == True and session.get('username') != None:
        result = "Nothing"
        if request.method == 'POST':
            if request.form['Button'] == 'Login':
                username  = request.form['username']
                password  = request.form['password']
                connection = getMysqlConnection()
                cursor = connection.cursor()
                sql =  'SELECT * FROM tmpUser WHERE `username` ="' + username + '" AND `password` ="' + password + '"'
                cursor.execute(sql)
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                password_db = result[2]
                if password_db == password:
                    output = "Succesfully Inserted Correct Credentials"
                    return render_template('sql_classic.html', output=output)
                output = result
                return render_template('sql_classic.html', output=output)
        output = result
        return render_template('sql_classic.html', output=output)
    return redirect(url_for('login'))

@app.route('/sql_blind', methods=['GET', 'POST'])
def sql_blind():
    if session.get('logged_in') == True and session.get('username') != None:
        result = "Nothing"
        if request.method == 'POST':
            if request.form['Button'] == 'Login':
                username  = request.form['username']
                password  = request.form['password']
                connection = getMysqlConnection()
                cursor = connection.cursor()
                sql =  'SELECT * FROM tmpUser WHERE `username` ="' + username + '" AND `password` ="' + password + '"'
                try:
                    cursor.execute(sql)
                except:
                    output = 'Nothing'
                    return render_template('sql_blind.html', output=output)
                result = cursor.fetchone()
                cursor.close()
                connection.close()
                password_db = result[2]
                if password_db == password:
                    output = "Succesfully Inserted Correct Credentials"
                    return render_template('sql_blind.html', output=output)
                output = result
                return render_template('sql_blind.html', output=output)
        output = result
        return render_template('sql_blind.html', output=output)
    return redirect(url_for('login'))

@app.route('/sql_add_tmp', methods=['GET', 'POST'])
def sql_tmpuser():
    if session.get('logged_in') == True and session.get('username') != None:
        if request.method == 'POST':
            if request.form['Button'] == 'CreateUser':
                username = request.form['username']
                password = request.form['password']
                if not ifExists(username):
                    connection = getMysqlConnection()
                    cursor = connection.cursor()
                    sql = "INSERT INTO `tmpUser` (`username`, `password`) VALUES (%s, %s)"
                    cursor.execute(sql, (username, password))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    output = "User " + username + " sucessfully added"
                    return render_template('sql_adduser.html', output=output)
                else:
                    output = "User " + username + " already exists"
                    return render_template('sql_adduser.html', output=output)
            elif request.form['Button'] == 'BackToSql':
                output = "Insert Valid Username and Password to Login"
                return render_template('sql_classic.html', output=output)
        output = "Start by Adding Credentials"
        return render_template('sql_adduser.html', output=output)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
