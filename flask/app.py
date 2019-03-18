from flask import Flask, request, render_template, session, redirect
import socket, os, json
import mysql.connector

app = Flask(__name__)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='172.17.0.1', port='3306', password='test123', database='mydb')


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
        connection = getMysqlConnection()
        cursor = connection.cursor()
        sql = "INSERT INTO `User` (`username`, `password`) VALUES (%s, %s)"


@app.route('/', methods=['GET', 'POST'])
def login():
    session['logged_in'] = False
    host = socket.gethostname()
    ip = "test"
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['password'] == '19970902':
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
            connection = getMysqlConnection()
            cursor = connection.cursor()
            username_form  = request.form['username']
            sql = "SELECT `id`, `password` FROM `User` WHERE `username`=%s"
            cursor.execute(sql, (username_form,))
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            if len(result) is 0:
                return render_template('login.html', output="Invalid Credentials Supplied")
            else:
                return render_template('test.html', result=result)
        elif request.form['Button'] == 'CreateUser':
            redirect('/adduser')
    else:
        output = "none"
        return render_template('login.html', output=output)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)
