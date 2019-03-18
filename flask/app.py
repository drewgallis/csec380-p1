from flask import Flask, request, render_template, session, redirect
import socket, os, json
from flask_wtf.csrf import CSRFProtect

from utils import *

app = Flask(__name__)
csrf = CSRFProtect(app)

@app.route('/testsql', methods=['GET', 'POST'])
def sqltest():
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
    if not session['logged_in']:
        return redirect('/login')
    else:
        host = socket.gethostname()
        ip = "test"
        return render_template('index.html', ip=ip, host=host)

#CSFR TOKEN PYTHON: http://flask.pocoo.org/snippets/3/
@app.route('/login', methods=['GET', 'POST'])
def login():
    session['logged_in'] = False
    session['username'] = None
    if request.method == 'POST':
        if request.form['Button'] == 'Login':
            username  = request.form['username']
            password  = request.form['password']
            session['username'] = username
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
                    return redirect('/')
                else:
                    output = "Password Supplied was invalid"
                    return render_template('login.html', output=output)
        elif request.form['Button'] == 'CreateUser':
            return redirect('/adduser')
    output = "Insert Valid Username and Password to Login"
    return render_template('login.html', output=output)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
