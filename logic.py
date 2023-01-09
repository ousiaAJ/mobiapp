from google import *
from share_calc import *


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
    time = time/3600
    tiR = int(time+0.5)
    kosten = auslesenPreis("XS", tiR, "N", km)
    answer1 = "Der Preis für die Fahrt beträgt: " + str(kosten) + "€.  "
    answer2 = "Die Strecke sind" + str(km) + "km"
    return answer1, answer2

def train(start, ziel, mode, datetime):
    result = direction(start, ziel, mode, datetime)
    res=json.loads(result)
    time = res['routes'][0]['legs'][0]['duration']['value']
    time = round((time/60),2)
    dauer = str(time)
    answer1 = "Die Fahrtdauer beträgt " + dauer + " Minuten"
    return answer1


