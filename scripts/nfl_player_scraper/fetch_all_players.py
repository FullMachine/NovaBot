import requests
import os

API_KEY = "85f4ef660cmsh2c8f98e6215486dp1da018jsn6615d8daf835"  # Your API-FOOTBALL key
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3/players"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def fetch_nfl_players():
    league_id = 1  # NFL
    season = 2023
    page = 1
    all_players = set()

    print("📥 Fetching NFL player names...")

    while True:
        url = f"{BASE_URL}?league={league_id}&season={season}&page={page}"
        response = requests.get(url, headers=headers)
        data = response.json()

        players = data["response"]
        if not players:
            break

        for item in players:
            name = item["player"]["name"]
            slug = name.lower().replace(".", "").replace("'", "").replace(" ", "-")
            all_players.add(slug)

        print(f"✅ Page {page} → {len(players)} players")
        page += 1

    os.makedirs("players", exist_ok=True)
    with open("players/nfl_players.txt", "w") as f:
        for player in sorted(all_players):
            f.write(player + "\n")

    print(f"✅ Saved {len(all_players)} players to players/nfl_players.txt")

if __name__ == "__main__":
    fetch_nfl_players()