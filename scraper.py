from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen

url = "https://www.kvb.koeln/fahrtinfo/betriebslage/bahn/"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

def scrape_KVB():
    response = urlopen(req).read()
    soup = BeautifulSoup(response, 'html.parser')
    rows = soup.findChildren(['main'])

    for row in rows:
        cells = row.findChildren('p')
        for cell in cells:
            text=cell.get_text()
        
    for row in rows:
        cells = row.findChildren('td')
        for cell in cells:
            text2=cell.get_text()
    
    
    return text, text2


""" result = scrape_KVB()
print (result) """



