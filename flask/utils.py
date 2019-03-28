import mysql.connector
import datetime as *
from flask import request
import requests
from werkzeug.security import generate_password_hash, check_password_hash

UPLOAD_FOLDER = '/etc/Videos'
ALLOWED_EXTENSIONS = set(['mp4', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mov'])

def download_url(url):
    if file and allowed_file(url):
        url = requests.args['url']
        r = requests.get(url)
        with app.open_instance_resource('downloade_file', 'wb') as f:
            f.write(r.connect)
        f.close()
    return
    
def get_timestamp():
    return datetime.now()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_hash(password):
    return generate_password_hash(password)

def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='172.17.0.1', port='3306', password='test123', database='mydb')

def ifExists(username):
    connection = getMysqlConnection()
    cursor = connection.cursor()
    sql = "SELECT `username` FROM `User` WHERE `username`=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return True
    return False
