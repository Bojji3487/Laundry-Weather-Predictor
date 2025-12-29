import os,requests

def get_coords(API_KEY):
    city=str(input("Enter city:"))
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": city,
        "limit": 1,
        "appid": API_KEY
    }

    geo_response = requests.get(url, params=params)
    geo_data = geo_response.json()

    if not geo_data:
        print("City not found")
        exit()

    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    return lat,lon