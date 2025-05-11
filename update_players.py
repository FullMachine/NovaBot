import requests
import time

API_KEY = "a61b1606-8b2c-499f-9425-eb65ed64a4bc"
BASE_URL = "https://api.balldontlie.io/v1/players"
HEADERS = {"Authorization": API_KEY}

def fetch_all_players():
    all_players = []
    cursor = None
    page_count = 1

    while True:
        url = f"{BASE_URL}?per_page=100"
        if cursor:
            url += f"&cursor={cursor}"

        print(f"📦 Fetching page {page_count} from BallDontLie API...")
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch page {page_count}, status: {response.status_code}")
            break

        data = response.json()
        players = data.get("data", [])
        meta = data.get("meta", {})

        for player in players:
            full_name = f"{player['first_name']} {player['last_name']}".lower()
            all_players.append(full_name)

        cursor = meta.get("next_cursor")
        if not cursor:
            break

        page_count += 1
        time.sleep(1)  # Be polite to the API

    return all_players

def save_players_to_file(players, filename="players.txt"):
    with open(filename, "w") as f:
        for name in players:
            f.write(name + "\n")
    print(f"✅ players.txt updated!\n🧍 Total players fetched: {len(players)}")

if __name__ == "__main__":
    print("🔄 Fetching NBA players from BallDontLie API...")
    players = fetch_all_players()
    save_players_to_file(players)