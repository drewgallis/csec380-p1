import pytest
import requests
from bs4 import BeautifulSoup

def webtest():
    r = requests.get('http://localhost:81')
    s = BeautifulSoup(r.text, 'html.parser')
    print(s.title.string)
    assert s.title.string == 'Hello World - 1'
    assert 'Hello World - 1' in r.text

webtest()