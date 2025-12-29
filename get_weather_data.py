import os,requests,json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

from get_coordinates import get_coords

API_KEY=os.getenv("API_KEY")


url = f"https://api.openweathermap.org/data/2.5/forecast"

lat,lon= get_coords(API_KEY)

params = {
    "lat": lat,
    "lon": lon,
    "exclude": "minutely,alerts",
    "units": "metric",
    "appid": API_KEY
}

weather_response = requests.get(url, params=params)
weather_data = weather_response.json()

weather_data=json.dumps(weather_data)

with open("datadump.json",'w') as f:
    f.write(weather_data)
