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
    cursor.execute(sql, ('test123', get_hash("test")))
    connection.commit()
    print("DB Added User:test123 " + "password:" + get_hash("test"))
    cursor.close()
    connection.close()
    
def webtest():
    initDB()
    options = Options() # get firefox webdriver options
    options.add_argument('-headless') # run tests in headless mode CMD
    firefox = Firefox(firefox_options=options) # intialize firefox web driver
    firefox.get('http://localhost:5000/login') # test against flask app
    user = firefox.find_element_by_name('username')
    user.send_keys('test123')
    password = firefox.find_element_by_name('password')
    password.send_keys("test")
    loginbtn = firefox.find_element_by_id('Login')
    loginbtn.click()
    assert "No results found." not in firefox.page_source
    print(firefox.page_source)
    firefox.close()
webtest()