from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import time
def get_hash(password):
    return generate_password_hash(password)

def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)
    
def getMysqlConnection():
    return mysql.connector.connect(user='root', host='172.17.0.1', port='33060', password='test123', database='mydb')

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
    return firefox

def upload_video(firefox, video_name):
    firefox.get('http://localhost:5000/') # test against flask app
    time.sleep(5)
    filename = firefox.find_element_by_name('filename')
    filename.send_keys(str(video_name))
    file_path = firefox.find_element_by_name('file')
    file_path.send_keys("C://luffytest.jpg")
    uploadBTN = firefox.find_element_by_id('UploadFile')
    uploadBTN.click()
    if "Successfully Uploaded File:" in firefox.page_source:
        print("Success Caught: File Uploaded Succesfully " + video_name)
    return firefox

def delete_video(firefox):
    try:
        firefox.get('http://localhost:5000/uploads/test123') # test against flask app
        deleteBTN = firefox.find_element_by_id('deleteVideo')
        deleteBTN.click()
        return True
    except:
        print("Failed to delete sample file")
    return

def main():
    #initDB()
    options = Options() # get firefox webdriver options
    options.add_argument('-headless') # run tests in headless mode CMD
    firefox = Firefox(firefox_options=options) # intialize firefox web driver
    firefox = getlogin(firefox)
    firefox = upload_video(firefox, "LuffyBoi")
    delete_video(firefox)
    firefox.close()

if __name__ == "__main__":
    main()