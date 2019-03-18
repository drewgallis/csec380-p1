from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import mysql.connector

def webtest():
    options = Options() # get firefox webdriver options
    options.add_argument('-headless') # run tests in headless mode CMD
    firefox = Firefox(firefox_options=options) # intialize firefox web driver
    firefox.get('http://localhost:5000') # test against flask app
    firefox.close()
webtest()