from selenium import webdriver

def webtest():
    firefox_opts = Options()  
    firefox_opts.add_argument("--headless")  
    driver = webdriver.Firefox(firefox_opts)
    driver.get('http://localhost')
    print driver.title
    driver.quit()

webtest()