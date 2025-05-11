import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")  # Make sure this is set in your .env or shell

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.american-football.api-sports.io"
}

output_file = "players/nfl_players.txt"
seen = set()
page = 1

with open(output_file, "w") as f:
    while True:
        print(f"Fetching page {page}")
        url = "https://v3.american-football.api-sports.io/players"
        params = {
            "league": 1,
            "season": 2023,
            "page": page
        }
        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()

        players = data.get("response", [])
        if not players:
            break

        for p in players:
            full_name = f"{p['player']['firstname']} {p['player']['lastname']}".lower()
            if full_name not in seen:
                seen.add(full_name)
                f.write(full_name + "\n")

        page += 1