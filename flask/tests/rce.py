from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import time

def get_hash(password):
    return generate_password_hash(password)
    
def getMysqlConnection():
    return mysql.connector.connect(user='root', host='172.17.0.1', port='33060', password='test123', database='mydb')

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

def ssti(firefox):
    print("Trying to perform Remote Code Execution..")
    firefox.get('http://localhost:5000/ssti?name=drew<script>alert("hello")</script>') # test against flask app
    try:
        alert = firefox.switch_to_alert()
        print("Success Caught: Alert text:" + alert.text)
        alert.accept()
        print("Success Caught: Valid Alert Screen")
        return firefox
    except:
        print("Error Caught: No Valid Alert Screen Found")
        return firefox

def main():
    options = Options() # get firefox webdriver options
    options.add_argument('-headless') # run tests in headless mode CMD
    firefox = Firefox(firefox_options=options) # intialize firefox web driver
    firefox = getlogin(firefox)
    firefox = ssti(firefox)
    firefox.close()

if __name__ == "__main__":
    main()