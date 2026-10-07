import cs50
from   flask    import Flask, render_template, redirect
from   datetime import date
import os
import requests
import sqlite3

app      = Flask(__name__)
API_KEY  = os.getenv("MY_API_KEY", "DEMO_KEY")
TODAY    = date.today().strftime("%Y-%m-%d")
URL      = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=TODAY&end_date=TODAY&api_key={API_KEY}"


@app.route("/")
def index():
    response         = requests.get(URL)
    status_code      = response.status_code
    asteroids_list   = []
    closest_distance = 7480000 # This is actually 0.5 astronomical units, NASA's standard for Neo
    total_count      = 0
    if status_code == 200:
        data = response.json()
        for item in data['near_earth_objects'][TODAY]:
            asteroids_list.append({
                "id":                item['id'],
                "name":              item['name'],
                "hazardous":         item['is_potentially_hazardous_asteroid'],
                "diameter":          float(item['estimated_diameter']['meters']['estimated_diameter_max']),
                "relative_velocity": float(item['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
                "miss_distance":     float(item['close_approach_data'][0]['miss_distance']['kilometers']),
                # Mathematical formula created for me by Gemini Pro 3.1 to calculate the threat level
                "threat_score":            round(min((((float(item['estimated_diameter']['meters']['estimated_diameter_max']) * float(item['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])) / float(item['close_approach_data'][0]['miss_distance']['kilometers'])) * 1000) + (15 if item['is_potentially_hazardous_asteroid'] == True else 0), 100.0), 1)  
                   
            })
            total_count += 1
            if item['close_approach_data'][0]['miss_distance']['kilometers'] < closest_distance:
                closest_distance = item['close_approach_data'][0]['miss_distance']['kilometers']
    else:
        return render_template("error.html", err = f"REQUEST DIDN'T SUCCEED! STATUS CODE: {status_code}!")
    # The descending sorting suggestion & lambda function was provided by Gemini Pro 3.1
    asteroids_list.sort(key = lambda x: x['threat_score'], reverse = True)
    return render_template("index.html", asteroids = asteroids_list, highest_threat = asteroids_list[0]['threat_score'])
