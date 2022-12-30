import requests
import pandas as pd
from datetime import datetime
import json

def direction(origin, destination, mode, when):

    when = datetime.strptime(when, '%Y-%m-%d %H:%M')
    timestamp = int(datetime.timestamp(when))
    print(timestamp)

    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&mode={mode}&transit_mode=tram&departure_time={timestamp}&key=AIzaSyB238rM6g9FmFf1EGDa40AOXXdG2wtcc9U"

    payload={}
    headers = {}
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)

    return(response.text)

#Launcher
#direction("Düsseldorf", "Koblenz", "transit", "21/Dec/2022 14:00:00")


def time_helper(ts):
# Timestamp Helper
    ts = 1671552844
    dt_object = datetime.fromtimestamp(ts)
    print(dt_object)
