import json
from collections import defaultdict
from datetime import datetime
import csv
import pandas as pd



with open('datadump.json','r') as f:
    data=json.load(f)


grouped = defaultdict(list)

for entry in data["list"]:
    date = entry["dt_txt"].split(" ")[0]  # "2025-12-30"
    grouped[date].append(entry)

daily_vars = {}

for date, hours in grouped.items():
    daily_vars[date] = {
        "temps": [],
        "clouds": [],
        "rain_probs": [],
        "is_day": [],
        "times": []
    }

    for h in hours:
        daily_vars[date]["temps"].append(h["main"]["temp"])
        daily_vars[date]["clouds"].append(h["clouds"]["all"])
        daily_vars[date]["rain_probs"].append(h["pop"])
        daily_vars[date]["is_day"].append(h["sys"]["pod"] == "d")
        daily_vars[date]["times"].append(h["dt_txt"])


for date, hours in grouped.items():
    morning = None

    for h in hours:
        if "09:00" in h["dt_txt"]:
            morning = h["main"]["temp"]
            break

    if morning is None:
        morning = hours[0]["main"]["temp"]

    daily_vars[date]["morning_temp"] = morning


for date, d in daily_vars.items():
    temps = d["temps"]

    d["temp_max"] = max(temps)
    d["temp_avg"] = sum(temps) / len(temps)

for date, d in daily_vars.items():
    temps = d["temps"]

    d["temp_min"] = min(temps)
    d["temp_range"] = d["temp_max"] - d["temp_min"]


#cloud penalty and effective hours
#Sun hours
for date, d in daily_vars.items():
    sun_blocks = sum(d["is_day"])#True =1 false = 0
    d["sun_hours"] = sun_blocks * 3


# effective sunlight, most important
for date, d in daily_vars.items():
    d["cloud_avg"] = sum(d["clouds"]) / len(d["clouds"])
    d["cloud_penalty"] = d["cloud_avg"] / 100
    d["effective_sun"] = d["sun_hours"] * (1 - d["cloud_penalty"])

with open("weather_training_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow ([
        "date",
        "sun_hours",
        "effective_sun",
        "temp_max",
        "temp_avg",
        "temp_min",
        "temp_range",
        "cloud_avg",
        "morning_temp"
    ])

    for date, d in daily_vars.items():
        writer.writerow([
            date,
            round(d["sun_hours"], 2),
            round(d["effective_sun"], 2),
            round(d["temp_max"], 2),
            round(d["temp_avg"], 2),
            round(d["temp_min"], 2),
            round(d["temp_range"], 2),
            round(d["cloud_avg"], 2),
            round(d["morning_temp"], 2)
        ])

df = pd.read_csv("weather_training_data.csv")

df["comfort_score"] = (
    0.35 * df["temp_max"]
  + 0.30 * df["effective_sun"]
  + 0.20 * df["temp_range"]
  - 0.15 * df["cloud_avg"]
)

df.to_csv("weighted_dataset.csv", index=False)
