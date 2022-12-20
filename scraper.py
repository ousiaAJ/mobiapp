from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen

url = "https://www.kvb.koeln/fahrtinfo/betriebslage/bahn/"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

def scrape_KVB():
    response = urlopen(req).read()
    soup = BeautifulSoup(response, 'html.parser')
    rows = soup.findChildren(['td'])
    return rows

""" results = scrape_KVB()
for item in results:
    text = item.get_text()
    print(text) """


