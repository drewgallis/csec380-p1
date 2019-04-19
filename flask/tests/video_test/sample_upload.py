from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import time
import os
    
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
    return firefox

def upload_video(firefox, video_name, file_name):
    firefox.get('http://localhost:5000/') # test against flask app
    time.sleep(5)
    filename = firefox.find_element_by_name('filename')
    filename.send_keys(str(video_name))
    file_path = firefox.find_element_by_name('file')
    path = "/home/travis/build/drewgallis/csec380-p1/flask/tests/video_test/" + file_name
    file_path.send_keys(path)
    uploadBTN = firefox.find_element_by_id('UploadFile')
    uploadBTN.click()
    if "Successfully Uploaded File:" in firefox.page_source:
        print("Success Caught: File Uploaded Succesfully " + video_name)
    return firefox

def delete_video(firefox, video_name):
    path = 'http://localhost:5000/uploads/delete/test123/' + video_name
    firefox.get(path) # test against flask app
    print("Trying to delete image...")
    if video_name not in firefox.page_source:
        print("Sucessfully Deleted File: " + video_name)
    else:
         print("Could NOT Deleted File: " + video_name)
    return firefox

def main():
    options = Options() # get firefox webdriver options
    options.add_argument('-headless') # run tests in headless mode CMD
    firefox = Firefox(firefox_options=options) # intialize firefox web driver
    firefox = getlogin(firefox)
    firefox = upload_video(firefox, "LuffyBoi", "luffy_test.jpg")
    firefox = upload_video(firefox, "Rabbit", "rabbit_test.jpg")
    firefox = delete_video(firefox, "LuffyBoi")
    delete_video(firefox, "Rabbit")
    firefox.close()

if __name__ == "__main__":
    main()