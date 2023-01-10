from google import *
from share_calc import *
from scraper import *


def selectSource(start, ziel, mode, datetime):
    if "driving" in mode:
        result = carshare(start, ziel, mode, datetime)
    elif "transit" in mode:
        result = train(start, ziel, mode, datetime)
    return result
        

def carshare(start, ziel, mode, datetime):
    result = direction(start, ziel, mode, datetime)
    res = json.loads(result)
    km = res['routes'][0]['legs'][0]['distance']['value']
    km = round(km/1000)
    time = res['routes'][0]['legs'][0]['duration']['value']
    ti = time/3600
    dauer = int(time/60)
    dauer = str(dauer)
    tiR = int(ti+0.5)
    kosten = auslesenPreis("XS", tiR, "N", km)
    answer1 = "Das gewählte Verkehrsmittel ist Auto." + " Der Preis für die Fahrt beträgt: " + str(kosten) + "€.  "
    answer2 = "Die Strecke beträgt " + str(km) + "km. " + "Die Fahrtzeit ist: " + dauer + " Minuten."
    return answer1, answer2

def train(start, ziel, mode, datetime):
    result = direction(start, ziel, mode, datetime)
    res=json.loads(result)
    time = res['routes'][0]['legs'][0]['duration']['value']
    time = int(time/60)
    dauer = str(time)
    ankunft = res['routes'][0]['legs'][0]['arrival_time']['text']
    answer1 = "Das gewählte Verkehrsmittel ist Zug." + " Die Fahrtdauer beträgt " + dauer + " Minuten. " + "Ankunft ist um: " + ankunft
    answer2 = scrape_KVB()
    return answer1, answer2

    


