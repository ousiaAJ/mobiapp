from google import *
from share_calc import *
from scraper import *
from nextbike import *


def selectSource(start, ziel, mode, datetime, selection):
    if "driving" in mode:
        result = carshare(start, ziel, mode, datetime)
    elif "transit" in mode:
        result = train(start, ziel, mode, datetime)
    elif "bus" in mode:
        result = bus(start, ziel, mode, datetime)
    elif "bicycling" in mode:
        result = bike(start, ziel, mode, datetime)
    elif "next" in mode:
        #print(start, selection)
        result = next(selection)
    return result
        

def carshare(start, ziel, mode, datetime):
    mo2=""
    result = direction(start, ziel, mode, mo2, datetime)
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
    mo2="rail"
    result = direction(start, ziel, mode, mo2, datetime)
    res=json.loads(result)
    time = res['routes'][0]['legs'][0]['duration']['value']
    time = int(time/60)
    dauer = str(time)
    ankunft = res['routes'][0]['legs'][0]['arrival_time']['text']
    answer1 = "Das gewählte Verkehrsmittel ist Zug." + " Die Fahrtdauer beträgt " + dauer + " Minuten. " + "Ankunft ist um: " + ankunft
    answer2 = scrape_KVB()
    return answer1, answer2

def bus(start, ziel, mode, datetime):
    mode=["transit"]
    mo2="bus"
    result = direction(start, ziel, mode, mo2, datetime)
    res=json.loads(result)
    time = res['routes'][0]['legs'][0]['duration']['value']
    time = int(time/60)
    dauer = str(time)
    ankunft = res['routes'][0]['legs'][0]['arrival_time']['text']
    answer1 = "Das gewählte Verkehrsmittel ist Bus." + " Die Fahrtdauer beträgt " + dauer + " Minuten. " + "Ankunft ist um: " + ankunft
    answer2 = scrape_KVB()
    return answer1, answer2

def bike(start, ziel, mode, datetime):
    mo2=""
    result = direction(start, ziel, mode, mo2, datetime)
    res=json.loads(result)
    km = res['routes'][0]['legs'][0]['distance']['text']
    dauer = res['routes'][0]['legs'][0]['duration']['text']
    answer1 = "Das gewählte Verkehrsmittel ist Fahrrad." + " Die Strecke beträgt " + km + " Minuten. "
    answer2 = "Fahrtdauer beträgt: " + dauer
    return answer1, answer2

def next(selection):
    result=nextbike(selection)
    if result == None:
        answer1 = "Leihstation " + selection
        answer2 = "Leider kein Fahrrad verfügbar"
    else:
        answer1 = "Anzahl der verfügbaren Fahrräder: "
        answer2 = result
    return answer1, answer2
