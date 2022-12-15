""" API Abfragen Sammlung"""
import http.client

def API_DB():
   conn = http.client.HTTPSConnection("apis.deutschebahn.com")
   headers = {
    'DB-Client-Id': "7eec6e17aa2db2b09d76c490202112ac",
    'DB-Api-Key': "a3854011cb83292f31f11cfa8da36ffe",
    'accept': "application/json"
    }
   conn.request("GET", "/db-api-marketplace/apis/fahrplan/v1/departureBoard/REPLACE_ID?date=2022-12-20", headers=headers)

   res = conn.getresponse()
   data = res.read()

   response = data.decode("utf-8")
   print(response)
   return response
