import json
import http.client

# DB API
def DB_API():
    def location():
        conn = http.client.HTTPSConnection("apis.deutschebahn.com")

        headers = {
        'DB-Client-Id': "7eec6e17aa2db2b09d76c490202112ac",
        'DB-Api-Key': "a3854011cb83292f31f11cfa8da36ffe",
        'accept': "application/json"
        }

        conn.request("GET", "/db-api-marketplace/apis/fahrplan/v1/location/Bonn", headers=headers)

        res = conn.getresponse()
        data = res.read()
        location = json.loads(data)
        code = location[0]["id"]
        timetable(code)

    def timetable(loc):
        conn = http.client.HTTPSConnection("apis.deutschebahn.com")
        print(loc)
        date = "2022-12-20"
        time = "T12:00"
        headers = {
        'DB-Client-Id': "7eec6e17aa2db2b09d76c490202112ac",
        'DB-Api-Key': "a3854011cb83292f31f11cfa8da36ffe",
        'accept': "application/json"
        }
        url = f"/db-api-marketplace/apis/fahrplan/v1/departureBoard/{loc}?date={date}{time}"
        print (url)
        conn.request("GET", url, headers=headers)

        res = conn.getresponse()
        data = res.read()
        result = json.loads(data)
        print(result)
    location()


# nextbike API

import requests 
import json
import datetime
import os
#import psycopg2
#import psycopg2.extras
import traceback
#import config
import time
import logging

def get_nextbike_locations ():
    
    # request data
    URL = "https://gbfs.nextbike.net/maps/gbfs/v1/nextbike_bn/en/free_bike_status.json"

    # sending get request and saving the response as response object 
    response = requests.get(url = URL) 
    try:
        r = response.json()
        nextbikes = []
        for i in range(len(r['data']['bikes'])):
            try:
                bike_id = int(r['data']['bikes'][i]['bike_id'])
            except:
                # single bike have no ID (?!); skip these bikes
                continue
            
            lat = r['data']['bikes'][i]['lat']
            lon = r['data']['bikes'][i]['lon']
            nextbikes.append([bike_id, NEXTBIKE, query_date, lat,lon])
        return nextbikes
    except Exception:
        logging.exception("message")
print (get_nextbike_locations())

def get_lidlbike_locations():

    #Berlin lat lon
    radius_center_lat=52.520008
    radius_center_lon=13.404954

    # request data
    URL = "https://api.deutschebahn.com/flinkster-api-ng/v1/bookingproposals"

    radius=10000 # radius in meter, max 10000 (10km)
    providernetwork=2
    expand='rentalObject'
    limit = 50

    offset = 0 # scroll with offset through pagination
    more_bikes = True
    key = config.key1

    lidlbikes = []
    while more_bikes:
        try:
        
            #header
            # note in header
            headers = {"Authorization": key, "Accept": "application/json"}

            # defining a params dict for the parameters to be sent to the API 
            PARAMS = {'lat':radius_center_lat, 'lon':radius_center_lon, 'radius':radius, 'providernetwork':providernetwork, 'expand':expand, 
            'limit':limit, 'offset':offset} 

            # sending get request and saving the response as response object 
            response = requests.get(url = URL, params = PARAMS, headers=headers) 

            r = response.json()

            # if bad response without items then skip
            if ('items' in r):
                for i in range(len(r['items'])):
                    bike_id = r['items'][i]['rentalObject']['providerRentalObjectId']
                    
                    # single bike have no ID (?!); skip these bikes
                    if not bike_id:
                        continue

                    lat = r['items'][i]['position']['coordinates'][1]
                    lon = r['items'][i]['position']['coordinates'][0]
                    lidlbikes.append([bike_id, LIDLBIKE, query_date, lat, lon])

                # get all paginations
                offset += 50
                if len(r['items']) < 50:
                    more_bikes = False

                # 30 calls max per minute (then timeout)
                if (offset % 3000 == 0):
                    key = config.key3
                elif (offset % 1500 == 0):
                    key = config.key2
            
            else:
                more_bikes = False


        except Exception:
            more_bikes = False
            logging.exception("message")
        
    return lidlbikes

def get_mobike_locations():

    # request data
    URL = "http://app.mobike.com/api/nearby/v4/nearbyBikeInfo"
    plattform= '1'

    # header
    headers = {"plattform": plattform, \
        "Content-Type": "application/x-www-form-urlencoded", \
        "User-Agent" : "Mozilla/5.0 (Android 7.1.2; Pixel Build/NHG47Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.9 NTENTBrowser/3.7.0.496 (IWireless-US) Mobile Safari/537.36"}

    radius_centers = pd.read_csv("coordinates.csv")

    mobikes = []
    for i in range (radius_centers.shape[0]):
        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {'latitude': radius_centers.iloc[i, 0], 'longitude': radius_centers.iloc[i, 1]}

        # sending get request and saving the response as response object 
        response = requests.get(url = URL, params = PARAMS, headers = headers) 

        #Todo error handling
        try:
            r = response.json()

            # if no error is returned, get bike information
            if r['code'] == 0:
            
                for i in range(len(r['bike'])):
                    bike_id = r['bike'][i]['distId'][1:]
                    lat = r['bike'][i]['distY']
                    lon = r['bike'][i]['distX']
                    mobikes.append([bike_id, MOBIKE, query_date, lat, lon])
            
            else:
                continue
        
        except Exception:
            logging.exception("message")
        
    return mobikes

""" if __name__== "__main__":
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logging.basicConfig(level=logging.INFO, filename="logfile.log")
    logger = logging.getLogger(__name__)

    # Connect to an existing database
    query_date= datetime.datetime.now()
    NEXTBIKE = 0
    LIDLBIKE = 1
    MOBIKE = 2

    nextbikes = get_nextbike_locations()

    lidlbikes = get_lidlbike_locations() """

    
   