from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen

url = "https://www.kvb.koeln/fahrtinfo/betriebslage/bahn/"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

def scrape_KVB():
    response = urlopen(req).read()
    soup = BeautifulSoup(response, 'html.parser')
    rows = soup.find_all('div', class_='container')
    temp = ["STÖRUNGSMELDUNGEN RAUM KÖLN:  "]

    for row in rows:
        cells = row.findChildren(class_='number red-text')
        for cell in cells:
            numbers=cell.prettify()
            #temp.append(numbers)
            #print(numbers)            

    for row in rows:
        cells = row.findChildren(class_='fliesstext')
        for cell in cells:
            text=cell.getText().replace("\n", "")
            temp.append(text)
        
    for row in rows:
        cells = row.findChildren(class_='table table-striped')
        for cell in cells:
            text2=cell.getText().replace("\n", "")
            temp.append(text2)
    #line_numbers = [int(temp) for temp in text2.split() if temp.isdigit()]
    answer = temp
    return (answer)

#Launcher
#result = scrape_KVB()
#print (result)



