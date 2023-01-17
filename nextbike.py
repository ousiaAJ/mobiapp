from bs4 import BeautifulSoup
#import lxml
import requests


#BS4

def nextbike(start_list):
    url = 'http://api.nextbike.net/maps/nextbike-live.xml?city=14'
    headers = {}
    payload = {}

    start = start_list
    response = requests.request("GET", url, headers=headers, data=payload)
    result = response.text

    soup = BeautifulSoup(result, "lxml-xml")
    #places_list = soup.find_all("place")
    #placenames = soup.get("name")
    places = soup.find("place", {"name": {start}} )
    bike = places.get("bikes_available_to_rent")
    return bike

#Launcher
#result = nextbike("Aldi Sürth")
#print(result)