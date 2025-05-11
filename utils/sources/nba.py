import requests
import os

def fetch_active_nba_players():
    print("📡 Fetching active NBA players from BallDontLie API...")

    url = "https://balldontlie.io/api/v1/players?per_page=100&page=1"
    players = []

    try:
        while url:
            response = requests.get(url)
            print("Response status:", response.status_code)
            print("Response text:", response.text[:500])

            data = response.json()
            players.extend(data["data"])

            # Go to next page
            if data["meta"]["next_page"]:
                url = f"https://balldontlie.io/api/v1/players?per_page=100&page={data['meta']['next_page']}"
            else:
                url = None

        print(f"✅ Saved {len(players)} players to players/nba_players.txt")
        os.makedirs("players", exist_ok=True)
        with open("players/nba_players.txt", "w") as f:
            for player in players:
                full_name = f"{player['first_name']} {player['last_name']}".strip().lower().replace(" ", "-")
                f.write(full_name + "\n")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    fetch_active_nba_players()