import mysql.connector
import datetime
from flask import request
import requests
from werkzeug.security import generate_password_hash, check_password_hash

UPLOAD_FOLDER = '/etc/Videos'
ALLOWED_EXTENSIONS = set(['mp4', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mov'])

def get_userid(username):
    connection = getMysqlConnection()
    cursor = connection.cursor()
    sql = "SELECT `id` FROM `User` WHERE `username`=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return str(result[0])

def get_users():
    connection = getMysqlConnection()
    cursor = connection.cursor()
    sql = "SELECT `username`, `url`,`video_name`,`time_stamp` FROM `VideoStats` LIMIT 50"
    cursor.execute(sql)
    result = cursor.fetchall()
    return result 
    
def download_url(url, path):
    r = requests.get(url, allow_redirects=True)
    with open(path, 'wb') as f:
        f.write(r.content)
        return True
    return False

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def get_timestamp():
    return datetime.datetime.utcnow()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_hash(password):
    return generate_password_hash(password)

def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='172.17.0.1', port='33060', password='test123', database='mydb')

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
 
def delete_video(username, video):
    #Check database to see if the user has this video
    #We store the path to the video so if video is just the name add /Videos/username/ to video
    video_name = "/Videos/" + str(username) + "/" + str(video)
    connection = getMysqlConnection()
    cursor = connection.cursor()
    sql = "SELECT `video_name` FROM `VideoStats` WHERE `username`=%s AND `video_name`=%s"
    cursor.execute(sql, (username, video_name))
    result = cursor.fetchone()
    connection.close()
    if result:
        #Delete the video in the database and in /Videos/username
        connection = getMysqlConnection()
        cursor = connection.cursor()
        sql = "DELETE FROM `VideoStats` WHERE `username`=%s AND video_name=%s"
        cursor.execute(sql, (username, video_name))
        os.remove(video_name)
        return True
    return False