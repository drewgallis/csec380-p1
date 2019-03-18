from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

def get_hash(password):
    return generate_password_hash(password)

def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)
    
def getMysqlConnection():
    return mysql.connector.connect(user='root', host='172.17.0.1', port='3306', password='test123', database='mydb')

def initDB():
    connection = getMysqlConnection()
    cursor = connection.cursor()
    sql = "INSERT INTO `User` (`username`, `password`) VALUES (%s, %s)"
    pw_hash = get_hash('test')
    cursor.execute(sql, ('test123', pw_hash))
    connection.commit()
    print("DB Added User:test123 " + "password:" + pw_hash)
    cursor.close()
    connection.close()
    
def webtest(username, password):
    options = Options() # get firefox webdriver options
    options.add_argument('-headless') # run tests in headless mode CMD
    firefox = Firefox(firefox_options=options) # intialize firefox web driver
    firefox.get('http://localhost:5000/login') # test against flask app
    user = firefox.find_element_by_name('username')
    user.send_keys(str(username))
    password = firefox.find_element_by_name('password')
    password.send_keys(str(password))
    loginbtn = firefox.find_element_by_id('Login')
    loginbtn.click()
    print(firefox.page_source)
    if "Main Page" in firefox.page_source:
        print("Success Caught: Valid User Login!")
    if "Username Supplied was invalid" in firefox.page_source:
        print("Error Caught: Username Supplied was invalid")
    if "Password Supplied was invalid" in firefox.page_source:
        print("Error Caught: Password Supplied was invalid")
    firefox.close()

def main():
    initDB()
    webtest('test123','test')       # valid user
    webtest("test123","1234")       # invalid password
    webtest("test","test")          # invalid username

if __name__ == "__main__":
    main()