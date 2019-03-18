import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

def get_hash(password):
    return generate_password_hash(password)

def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='mariadb', port='3306', password='test123', database='mydb')

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