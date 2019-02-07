from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def webtest():
    firefox_opts = Options()  
    firefox_opts.headless = True
    driver = webdriver.Firefox(firefox_opts)
    driver.get('http://localhost')
    print driver.title
    driver.quit()

webtest()