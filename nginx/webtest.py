import pytest
import requests
from bs4 import BeautifulSoup

def webtest():
    req = requests.get('http://localhost:81')
    soup = BeautifulSoup(req.content, 'html.parser')
    textContent = []
    for i in range(0, 20):
    paragraphs = soup.find_all("p")[i].text
    textContent.append(paragraphs)
    print(paragraphs)
    
webtest()