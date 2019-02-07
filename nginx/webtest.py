from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

def webtest():
    opts = Options()
    opts.set_headless()
    assert opts.headless  #checking for headless mode
    firefox = Firefox(firefox_options=options)
    firefox.get('http://localhost')
webtest()