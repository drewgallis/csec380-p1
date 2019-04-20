from flask import Flask, request, render_template, session, redirect, url_for, render_template_string
import socket, os, json
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from utils import *

from jinja2 import Environment #addition for RCE
Jinja2 = Environment()  # addition for RCE

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['WEB_DIRECTORY'] = "/static/Videos"
app.config['OS_UPLOAD'] = "/app/static/Videos"
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
                return redirect(url_for('login'))
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
        username = session.get('username')
        p = str(app.config['OS_UPLOAD']) + '/' + str(session.get('username')) #make user specific path in Videos
        if os.path.exists(p) != True:
            os.mkdir(p)                 #Create user specific dir for user if it doesnt already exist
        if request.method == 'POST':
            userid = int(get_userid(session.get('username')))
            file_name = request.form['filename']
            output = " Please Insert a Valid Filename"
            if request.form['Type'] == 'uploadfile' and file_name:
                    # check if the post request has the file part
                if 'file' not in request.files:
                    output = "No file part"
                    return render_template('index.html', output=output, username=username)
                file = request.files['file']
                if file.filename == '':
                    output = "No selected file"
                    return render_template('index.html', output=output, username=username)
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
                    return render_template('index.html', output=output, username=username)
            if request.form['Type'] == 'uploadurl' and file_name:
                p = str(app.config['OS_UPLOAD']) + '/' + str(session.get('username')) #make user specific path in Videos
                if os.path.exists(p) != True:
                    os.mkdir(p)                 #Create user specific dir for user if it doesnt already exist
                    if 'url'not in request.form:
                        output = "No file part"
                        return render_template('index.html', output=output, username=username)
                url = request.form['url']
                filename = None
                if url != '':
                    if url.find('/'):
    	                filename = url.rsplit('/', 1)[1]
                    if url == '' or filename is None:
                        output = "No URL inputted or incorrect format"
                        return render_template('index.html', output=output, username=username)
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
                            return render_template('index.html', output=output, username=username)
                        output = "Could not upload url: " + filename
                        return render_template('index.html', output=output, username=username)
                    else:
                        return render_template('index.html', output='Content not supported', username=username)
                else:
                    return render_template('index.html', output='Please insert a URL', username=username)
        return render_template('index.html', output=output, username=username)
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
@app.route('/uploads')
def all_videos():
    if session.get('logged_in') == True and session.get('username') != None:
        users = os.listdir("/app/static/Videos/")
        return render_template("uploads.html", users = users)
    return redirect(url_for('login'))

# still need to implement  
@app.route('/uploads/<username>')
def user_videos(username=None):
    if session["username"] == username:
        listVideos=[]
        listImages=[]
        if session.get('logged_in') == True and session.get('username') != None:
            full_path = os.path.join(app.config['WEB_DIRECTORY'], username)
            files = os.listdir("/app/static/Videos/" + username)
            for file_name in files:
                video_name = get_video(file_name,username)
                final_path = full_path + "/" + file_name
                if ".mp4" in file_name or ".mov" in file_name:
                    listVideos.append({"path": final_path, "name": video_name})
                if ".jpg" in file_name or ".png" in file_name or ".jpeg" in file_name or ".gif" in file_name:
                    listImages.append({"path": final_path, "name": video_name})
            return render_template("uploads.html", output=files, listVideos=listVideos, listImages=listImages, user=username, canDelete="true")
    else:
        listVideos=[]
        listImages=[]
        if session.get('logged_in') == True and session.get('username') != None:
            full_path = os.path.join(app.config['WEB_DIRECTORY'], username)
            files = os.listdir("/app/static/Videos/" + username)
            for file_name in files:
                video_name = get_video(file_name,username)
                final_path = full_path + "/" + file_name
                if ".mp4" in file_name or ".mov" in file_name:
                    listVideos.append({"path": final_path, "name": video_name})
                if ".jpg" in file_name or ".png" in file_name or ".jpeg" in file_name or ".gif" in file_name:
                    listImages.append({"path": final_path, "name": video_name})
            return render_template("uploads.html", output=files, listVideos=listVideos, listImages=listImages, user=username, canDelete="false")
    return redirect(url_for('login'))

@app.route('/uploads/delete/<user>/<path>')
def delete_user_path(user, path): 
    delete_video(user, path)
    return redirect('/uploads/'+ user)

# still need to implement
@app.route('/search', methods=['GET', 'POST'])
def search():
    if session.get('logged_in') == True and session.get('username') != None:
        result = get_users()
        connection = getMysqlConnection()
        cursor = connection.cursor()
        sql = "SELECT `video_name`, `url`, `username` FROM `VideoStats`"
        cursor.execute(sql)
        result = cursor.fetchall()
        connection.close()
        files = {}
        videos = []
        users = []
        search_term = None
        if request.method == 'POST':
            if request.form['search_item'] != ' ':
                search_term  = request.form['search_item']
        # for user in result 
        for value in result:
            video_name= value[0]
            url= value[1]
            username= value[2]
            if search_term is not None:
                if search_term in video_name:
                    if username not in users:
                        files[username]= []
                        users.append(username)
                    files[username].append({"name":video_name, "url":url})
            else:
                if username not in users:
                    files[username]= []
                    users.append(username)
                files[username].append({"name":video_name, "url":url})
        return render_template('search.html', files=files)
    return redirect(url_for('login'))

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

# 404 catch
@app.errorhandler(404)
def page_not_found(e):
    page = request.base_url
    ### 404 LOGGER ####
    return render_template('404.html', page=page), 404

@app.errorhandler(500)
def error_overload(e):
    page = request.base_url
    msg = e
    return render_template('500.html', page=page, msg=msg), 500

# REMOTE CODE EXECUTION WORKING
@app.route("/ssti") 
def ssti():

    name = request.values.get('name')
    
    # SSTI VULNERABILITY
    # The vulnerability is introduced concatenating the
    # user-provided `name` variable to the template string.
    output = Jinja2.from_string('Hello ' + name + '!').render()
    
    # Instead, the variable should be passed to the template context.
    # Jinja2.from_string('Hello {{name}}!').render(name = name)

    return output

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=False, host='0.0.0.0', port=5000)
