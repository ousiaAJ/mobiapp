import requests
import json

def getWeather(start):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={start}&appid=beeb8f10394e934265050f0207d6e4d4&units=metric"
    response = requests.get(url)
    res = response.json()
    #print(res)
    y = res["main"]
    current_temperature = y["temp"]
    felt_temp = y["feels_like"]
    x = res["wind"]
    wind = x["speed"]
    z = res["weather"]
    weather_description = z[0]["description"]
    if "cloud" in weather_description:
        weather = "wolkig"
    elif "rain" in weather_description:
        weather = "regnerisch"
    elif "sun" in weather_description:
        weather = "sonnig"
    elif "snow" in weather_description:
        weather = "Schnee"
    elif "clear" in weather_description:
        weather = "klarer Himmel"
    elif "mist" in weather_description:
        weather = "neblig"

    answer1 = " Die Temperatur in Grad Celsius beträgt: " + str(current_temperature) + ", " + " gefühlt: " + str(felt_temp) + ". " 
    answer2 = " Wetterbeschreibung:  " + str(weather) + ". Wind: " + str(wind) + " km/h"
    back = answer1 + answer2
    return back

# Launcher
#answer = getWeather("Köln")
#print(answer)



