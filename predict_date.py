import json
from collections import defaultdict
from datetime import datetime


with open('datadump.json','r') as f:
    data=json.load(f)


grouped = defaultdict(list)

for entry in data["list"]:
    date = entry["dt_txt"].split(" ")[0]  # "2025-12-29"
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

print(json.dumps(daily_vars,indent=1))