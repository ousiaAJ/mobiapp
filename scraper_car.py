from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen

url = "https://www1.wdr.de/verkehr/nrw/meldungen/index.html"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

def scrape_WDR():
    response = urlopen(req).read()
    soup = BeautifulSoup(response, 'html.parser')
    rows = soup.find_all('div', class_='td')
    temp = ["STÖRUNGSMELDUNGEN AUTO:  "]

    for row in rows:
        cells = row.findChildren(class_='number red-text')
        for cell in cells:
            numbers=cell.prettify()
            #temp.append(numbers)
            #print(numbers)            

    for row in rows:
        cells = row.findChildren(class_='meldung')
        for cell in cells:
            text=cell.getText().replace("\n", "")
            temp.append(text)
        
    #line_numbers = [int(temp) for temp in text2.split() if temp.isdigit()]
    answer = temp
    return answer

#Launcher
result = scrape_WDR()
print (result)



