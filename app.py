import requests
from flask import Flask, render_template, request
import json
app = Flask(__name__)
heroes = []
with open("heroes.json") as json_file:
    heroes = json.load(json_file)

@app.route("/")
def index():
    hero_names = {}
    for hero in heroes:
        hero_names[hero['id']] = hero['localized_name']
    return render_template("index.html", hero_names=hero_names)

@app.route("/submit", methods=["POST"])
def submit_form():
    teama = "&".join(map(lambda p: f"teamA={p}", request.form.getlist('radiant_heroes[]')))
    teamb = "&".join(map(lambda p: f"teamB={p}", request.form.getlist('dire_heroes[]')))
    url = f"https://api.opendota.com/api/findMatches?{teama}&{teamb}"
    print(url)
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("httperr")
        found_matches = response.json()
    except:
        return "Error on Opendota's side!"

    found_matches.reverse()
    return_string = "<h3>Sorted from newest to oldest!</h3><ol>"
    winner_d = {
        True: "Radiant",
        False: "Dire"
    }
    for match in found_matches:
        return_string += '<li>match_id: <a href="https://www.opendota.com/matches/'+str(match['match_id'])+'">'+str(match['match_id'])+'</a>, winner: '+winner_d[match['teamawin']]+"</li>"
    return_string+="</ol>"
    return return_string