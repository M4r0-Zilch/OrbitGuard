from   cs50     import SQL
from   dotenv   import load_dotenv
from   flask    import Flask, render_template, redirect, request
from   datetime import date
import os
import requests

app      = Flask(__name__)
db       = SQL("sqlite:///orbitguard.db")
load_dotenv()
API_KEY  = os.getenv("API_KEY", "DEMO_KEY")
TODAY    = date.today().strftime("%Y-%m-%d")
URL      = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={TODAY}&end_date={TODAY}&api_key={API_KEY}"

def get_asteroids():
    response         = requests.get(URL)
    status_code      = response.status_code
    asteroids_list   = []
    closest_distance = 7480000 # This is actually 0.5 astronomical units, NASA's standard for Neo
    total_count      = 0
    hazardous        = 0
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
                # Mathematical formula for calculating the threat level
                "threat_score":            round(min((((float(item['estimated_diameter']['meters']['estimated_diameter_max']) * float(item['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])) / float(item['close_approach_data'][0]['miss_distance']['kilometers'])) * 1000) + (15 if item['is_potentially_hazardous_asteroid'] == True else 0), 100.0), 1)  
                       
            })
            total_count += 1
            if float(item['close_approach_data'][0]['miss_distance']['kilometers']) < closest_distance:
                closest_distance = round(float(item['close_approach_data'][0]['miss_distance']['kilometers']), 4)
            if item['is_potentially_hazardous_asteroid']:
                hazardous += 1
    else:
        return status_code

    asteroids_list.sort(key = lambda x: x['threat_score'], reverse = True)
    return {
        "asteroids_list": asteroids_list,
        "closest_distance": closest_distance,
        "hazardous": hazardous,
        "highest_threat": asteroids_list[0]['threat_score'],
        "total_count": total_count
        }

@app.route("/")
def index():
    data = get_asteroids()
    if isinstance(data, dict):
        asteroids_list = data['asteroids_list']
        hazardous = data['hazardous']
        closest_distance = data['closest_distance']
        highest_threat = data['highest_threat']
        total_count = data['total_count']
        return render_template("index.html", asteroids = asteroids_list, closest_distance = closest_distance, hazardous = hazardous, highest_threat = highest_threat, total_count = total_count)
    else:
        return render_template("error.html", err = f"REQUEST DIDN'T SUCCEED! STATUS CODE: {data}!")

@app.route("/pin", methods = ['POST'])
def pin():
    name          = request.form.get("asteroid_name")
    asteroid_id   = request.form.get("asteroid_id")
    threat        = request.form.get("threat_score")
    miss_distance = request.form.get("miss_distance")
    db.execute("INSERT OR IGNORE INTO pinned_targets (asteroid_id, name, threat_score, miss_distance) VALUES (?, ?, ?, ?)", asteroid_id, name, threat, miss_distance)
    return redirect("/")

@app.route("/watchlist", methods = ['POST', 'GET'])
def watchlist():
    pinned = db.execute("SELECT * FROM pinned_targets")
    return render_template("watchlist.html", pinned = pinned)

@app.route("/unpin", methods = ['GET', 'POST'])
def unpin():
    asteroid_id = request.form.get("asteroid_id")
    db.execute("DELETE FROM pinned_targets WHERE asteroid_id = ?", asteroid_id)
    return redirect("/watchlist")

@app.route("/chart")
def chart():
    data = get_asteroids()
    if isinstance(data, dict):
        asteroids_list = data['asteroids_list']
        return render_template("chart.html", asteroids = asteroids_list)
    else:
        return render_template("error.html", err = f"REQUEST DIDN'T SUCCEED! STATUS CODE: {data}!")
    