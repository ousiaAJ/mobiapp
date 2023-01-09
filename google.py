import requests
import pandas as pd
from datetime import datetime
import json

def direction(origin, destination, mode, when):

    when = datetime.strptime(when, '%Y-%m-%d %H:%M')
    timestamp = int(datetime.timestamp(when))

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={mode}&transit_mode=tram&departure_time={timestamp}&key=AIzaSyB238rM6g9FmFf1EGDa40AOXXdG2wtcc9U"

    payload={}
    headers = {}
   # print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    #print(response.status_code)
    return(response.text)

#Launcher
#result=direction("Düsseldorf", "Koblenz", "transit", "2023-01-22 14:00")
#print(result)


def time_helper(ts):
# Timestamp Helper
    ts = 1671552844
    dt_object = datetime.fromtimestamp(ts)
    print(dt_object)
