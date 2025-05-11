import requests
import time
import os

API_KEY = "J2tfndW5bg_24JEKSeDr4hfxSecvf4uS8MrSSkZKm6thvF72Ncw"
API_URL = "https://api.pandascore.co/players"
OUTPUT_PATH = "players/esports_players.txt"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

def fetch_esports_players():
    print("🎮 Fetching Esports players from PandaScore...")
    all_players = []
    page = 1
    per_page = 50

    while True:
        try:
            response = requests.get(
                f"{API_URL}?page={page}&per_page={per_page}",
                headers=HEADERS,
                timeout=10
            )
            if response.status_code != 200:
                print(f"❌ Error {response.status_code}: {response.text}")
                break

            data = response.json()
            if not data:
                break

            for player in data:
                name = player.get("name")
                if name:
                    all_players.append(name.lower())

            print(f"📦 Fetched page {page}")
            page += 1

            # TEST: stop after 5 pages max to prevent hang
            if page > 5:
                break

            time.sleep(1)

        except requests.exceptions.Timeout:
            print("❌ Timeout! PandaScore API is too slow.")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            break

    # Save results
    os.makedirs("players", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        for player in all_players:
            f.write(player + "\n")

    print(f"✅ Saved {len(all_players)} esports players to {OUTPUT_PATH}")

# Run it
fetch_esports_players()