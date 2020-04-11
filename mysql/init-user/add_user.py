import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

def add_user(username, password):
    pw_hash = get_hash(password)
    connection = getMysqlConnection()
    cursor = connection.cursor()
    sql = "INSERT INTO `User` (`username`, `password`) VALUES (%s, %s)"
    cursor.execute(sql, (username, pw_hash))
    connection.commit()
    cursor.close()
    connection.close()
    output = "User " + username + " sucessfully added"
    print(output)
    return

def get_hash(password):
    return generate_password_hash(password)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='mariadb', port='3306', password='test123', database='mydb')

def main():
    username = "Drew"
    password = "RobClem19970902_"
    add_user(username, password)

if __name__ == "__main__":
    main()