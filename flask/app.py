from flask import Flask, request, render_template, session, redirect
import socket, os, json
from utils import *

app = Flask(__name__)

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
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    sql = "SELECT `id`, `password` FROM `User` WHERE `username`=%s"
    cursor.execute(sql, ('test123',))
    result = cursor.fetchone()
    print(result)
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
def login():
    session['logged_in'] = False
    host = socket.gethostname()
    ip = "test"
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == '19970902':
            session['logged_in'] = True
            return redirect('/testsql')
        else:
            session['logged_in'] = False

    return render_template('auth.html', ip=ip, host=host)

#CSFR TOKEN PYTHON: http://flask.pocoo.org/snippets/3/
@app.route('/login', methods=['GET', 'POST'])
def logintest():
    session['logged_in'] = False

    if request.method == 'POST':
        if request.form['Button'] == 'Login':
            username  = request.form['username']
            password  = request.form['password']
            if not ifExists(username):
                output = "Username/Password Supplied was invalid"
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
                    return render_template('test.html', result="Sucessful Login")
                else:
                    output = "Username/Password Supplied was invalid"
                    return render_template('login.html', output=output)
        elif request.form['Button'] == 'CreateUser':
            return redirect('/adduser')
    output = "Insert Valid Username and Password to Login"
    return render_template('login.html', output=output)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
