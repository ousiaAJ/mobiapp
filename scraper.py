from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen

url = "https://www.kvb.koeln/fahrtinfo/betriebslage/bahn/"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

def scrape_KVB():
    response = urlopen(req).read()
    soup = BeautifulSoup(response, 'html.parser')
    rows = soup.find_all('div', class_='container')
    #print(rows)

    for row in rows:
        cells = row.findChildren(class_='fliesstext')
        for cell in cells:
            text=cell.text
        
    for row in rows:
        cells = row.findChildren(class_='table table-striped')
        for cell in cells:
            text2=cell.text
    answer = text + text2
    return answer


#result = scrape_KVB()
#print (result)



