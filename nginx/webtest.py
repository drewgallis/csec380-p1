import pytest
import requests
from bs4 import BeautifulSoup

def webtest():
    req = requests.get('http://localhost:81')
    soup = BeautifulSoup(req.text, 'html.parser')
    print(soup.p.string)
    assert s.title.string == 'Hello World - 1'
    assert 'Hello World - 1' in r.text

webtest()