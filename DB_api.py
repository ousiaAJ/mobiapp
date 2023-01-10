import json
import http.client

# DB API
def DB_API():
    def location():
        print("running")
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

    def timetable(loc, datetime):
        conn = http.client.HTTPSConnection("apis.deutschebahn.com")
        print(loc)
        date = "2023-02-20"
        time = "T12:00"
        headers = {
        'DB-Client-Id': "7eec6e17aa2db2b09d76c490202112ac",
        'DB-Api-Key': "a3854011cb83292f31f11cfa8da36ffe",
        'accept': "application/json"
        }
        url = f"/db-api-marketplace/apis/fahrplan/v1/departureBoard/{loc}?date={datetime}"
        print (url)
        conn.request("GET", url, headers=headers)

        res = conn.getresponse()
        data = res.read()
        result = json.loads(data)
        print(result)
    location()
#DB_API()



   