# scripts/fetch_nfl_players.py

import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")  # or paste your key directly
LEAGUE_ID = 1  # NFL
SEASON = 2023  # change this if needed

url = f"https://v3.american-football.api-sports.io/players?league={LEAGUE_ID}&season={SEASON}"
headers = {
    "x-apisports-key": API_KEY
}

players = []
page = 1

while True:
    response = requests.get(f"{url}&page={page}", headers=headers)
    data = response.json()

    for item in data['response']:
        name = item['player']['name']
        team = item['statistics'][0]['team']['name']
        players.append(f"{name} - {team}")

    if page >= data['paging']['total']:
        break
    page += 1

with open("players/nfl_players.txt", "w") as f:
    for player in players:
        f.write(player + "\n")

print(f"✅ Fetched {len(players)} NFL players.")