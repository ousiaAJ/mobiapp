from google import *
from share_calc import *
from scraper import *
from nextbike import *
from weather import *
from datetime import datetime




def selectSource(start, ziel, mode, datetime, selection):
    result = []
    weather = getWeather(start)
    result.append(weather)
    if mode ==['driving']:
        result1 = carshare(start, ziel, mode, datetime)
        result.append(result1)
    elif mode == ['transit']:
        result2 = train(start, ziel, mode, datetime)
        result.append(result2)
    elif mode == ['bus']:
        result3 = bus(start, ziel, mode, datetime)
        result.append(result3)
    elif mode == ['bicycling']:
        result4 = bike(start, ziel, mode, datetime)
        result.append(result4)
    elif mode == ['next']:
        result5 = next(start, ziel, datetime, selection)
        result.append(result5)
    elif mode == ['transit', 'bus']:
        result2 = train(start, ziel, ['transit'], datetime)
        result3 = bus(start, ziel, ['bus'], datetime)
        result.append(result2)
        result.append(result3)
    elif mode == ['transit', 'bicycling']:
        result2 = train(start, ziel, ['transit'], datetime)
        result4 = bike(start, ziel, ['bicycling'], datetime)
        result.append(result2)
        result.append(result4)
    elif mode == ['transit', 'next']:
        result2 = train(start, ziel, ['transit'], datetime)
        result5 = next(start, ziel, datetime, selection)
        result.append(result2)
        result.append(result5)
    elif mode == ['bus', 'bicycling']:
        result3 = bus(start, ziel, ['bus'], datetime)
        result4 = bike(start, ziel, mode, datetime)
        result.append(result3)
        result.append(result4)
    elif mode == ['bus', 'next']:
        result3 = bus(start, ziel, ['bus'], datetime)
        result.append(result3)
        result5 = next(start, ziel, datetime, selection)
        result.append(result5)
    else:
        result.append("Kombination nicht verfügbar")

    return result


def carshare(start, ziel, mode, datetime):
    mo2=""
    result = direction(start, ziel, mode, mo2, datetime)
    res = json.loads(result)
    #print(result)
    km = res['routes'][0]['legs'][0]['distance']['value']
    km = round(km/1000)
    time = res['routes'][0]['legs'][0]['duration']['value']
    ti = time/3600
    dauer = int(time/60)
    tiR = int(ti+0.75)
    kosten = auslesenPreis("XS", tiR, "N", km)
    co2 = str(km * 0.180) 
    answer1 = "Das gewählte Verkehrsmittel ist Auto." + " Der Preis für die Fahrt beträgt: " + str(kosten) + "€.  "
    answer2 = "Die Strecke beträgt " + str(km) + "km. " + "Die Fahrtzeit ist: " + str(dauer) + " Minuten. " "Deine CO2 Emmission beträgt " + co2 + " kg"
    return answer1, answer2

def train(start, ziel, mode, datetime):
    print(start, ziel, mode, datetime)
    mo2="rail"
    result = direction(start, ziel, mode, mo2, datetime)
    res=json.loads(result)
    time = res['routes'][0]['legs'][0]['duration']['value']
    time = int(time/60)
    dauer = str(time)
    km = res['routes'][0]['legs'][0]['distance']['value']
    km = round(km/1000)
    co2 = str(km * 58)
    ankunft = res['routes'][0]['legs'][0]['arrival_time']['value']
    an = int(ankunft)
    zeit = zeitrechner(an)
    answer1 = "Das gewählte Verkehrsmittel ist Zug." + " Die Fahrtdauer beträgt " + dauer + " Minuten. " + "Ankunft ist um: " + str(zeit) + " Die CO2 Emmissionen betragen " + co2 + " g."
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
    ankunft = res['routes'][0]['legs'][0]['arrival_time']['value']
    an = int(ankunft)
    zeit = zeitrechner(an)
    km = res['routes'][0]['legs'][0]['distance']['value']
    km = round(km/1000)
    co2 = str(km * 80)
    answer1 = "Das gewählte Verkehrsmittel ist Bus." + " Die Fahrtdauer beträgt " + dauer + " Minuten. " + "Ankunft ist um: " + zeit + " Die CO2 Emmissionen betragen " + co2 + " g."
    answer2 = scrape_KVB()
    return answer1, answer2

def bike(start, ziel, mode, datetime):
    mo2=""
    result = direction(start, ziel, mode, mo2, datetime)
    res=json.loads(result)
    km = res['routes'][0]['legs'][0]['distance']['text']
    dauer = res['routes'][0]['legs'][0]['duration']['text']
    answer1 = "Das gewählte Verkehrsmittel ist Fahrrad." + " Die Strecke beträgt " + km + "Deine CO2 Emmission beträgt 0g."
    answer2 = "Fahrtdauer beträgt: " + dauer
    return answer1, answer2

def next(start, ziel, datetime, selection):
    result=nextbike(selection)
    if result == None:
        answer1 = "Leihstation " + selection + ". Leider kein Fahrrad verfügbar"
    else:
        answer1 = "Anzahl der verfügbaren Fahrräder: " + result        
    mode=["bicycling"]
    mo2=""
    result2 = direction(start, ziel, mode, mo2, datetime)
    res2 = json.loads(result2)
    dauer = res2['routes'][0]['legs'][0]['duration']['value']
    fahrzeit = "Die Fahrtzeit mit Fahrrad beträgt: " + str(int(dauer/60)) + " Minuten. " + "Deine CO2 Emmission beträgt 0g."
    preis = (dauer/60)/15
    preis = "Der Leihpreis beträgt: " + str(round(preis)) + " Euro"
    return answer1, fahrzeit, preis


def zeitrechner(ts):
    dt_object = datetime.fromtimestamp(ts)
    ts = str(dt_object)
    zeit = ts.split(" ")
    return (zeit[1])

""" def testfunc(start, ziel, mode, mo2, datetime):
    result = direction(start, ziel, mode, mo2, datetime)
    res = json.loads(result)
    ankunft = res['routes'][0]['legs'][0]['arrival_time']['text']
    print(ankunft) """

# Launcher Test
#testresult = train("Köln", "Bonn", "transit", "2023-01-22 14:00")
#print(testresult)