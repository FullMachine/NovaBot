import requests
import os

output_path = "players/soccer_players.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

headers = {
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    "x-rapidapi-key": "85f4ef660cmsh2c8f98e6215486dp1da018jsn6615d8daf835"
}

# Premier League 2023 season = ID 39
def fetch_soccer_players():
    all_players = []
    for page in range(1, 6):  # Get 5 pages
        url = f"https://api-football-v1.p.rapidapi.com/v3/players?league=39&season=2023&page={page}"
        response = requests.get(url, headers=headers)
        data = response.json()

        if "response" in data:
            for item in data["response"]:
                player = item["player"]
                name = player.get("name")
                if name:
                    all_players.append(name.strip())

    with open(output_path, "w", encoding="utf-8") as f:
        for name in sorted(set(all_players)):
            f.write(name + "\n")

    print(f"✅ Saved {len(all_players)} soccer players to {output_path}")

if __name__ == "__main__":
    fetch_soccer_players()