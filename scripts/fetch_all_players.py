import requests
import os
from datetime import datetime

# API keys
BALDONTLIE_API_KEY = "a61b1606-8b2c-499f-9425-eb65ed64a4bc"
HEADERS = {"Authorization": BALDONTLIE_API_KEY}

# Output folder
OUTPUT_FOLDER = "players"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def save_players_to_file(sport, players):
    filename = os.path.join(OUTPUT_FOLDER, f"{sport.lower()}_players.txt")
    with open(filename, "w", encoding="utf-8") as f:
        for player in players:
            full_name = f"{player['first_name']} {player['last_name']}".strip()
            f.write(full_name.lower() + "\n")
    print(f"✅ Saved {len(players)} {sport.upper()} players to {filename}")

def fetch_nba_players():
    print("📦 Fetching NBA players from BallDontLie...")
    all_players = []
    base_url = "https://api.balldontlie.io/v1/players"
    cursor = None

    while True:
        url = base_url + "?per_page=100"
        if cursor:
            url += f"&cursor={cursor}"

        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"[ERROR] Status {response.status_code} for NBA")
            break

        data = response.json()
        players = data.get("data", [])
        if not players:
            break

        all_players.extend(players)
        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            break

    save_players_to_file("nba", all_players)

if __name__ == "__main__":
    print("🟢 Running multi-sport player fetcher...")
    fetch_nba_players()
    print("✅ All done.")