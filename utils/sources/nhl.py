import requests
import os

output_path = "players/nhl_players.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

teams = {
    "Toronto Maple Leafs": "134880",
    "Boston Bruins": "134872",
    "Chicago Blackhawks": "134876",
    "New York Rangers": "134875",
    "Los Angeles Kings": "134873",
    "Pittsburgh Penguins": "134874"
}

def fetch_nhl_players():
    all_players = []

    for team_name, team_id in teams.items():
        url = f"https://www.thesportsdb.com/api/v1/json/3/lookup_all_players.php?id={team_id}"
        response = requests.get(url)
        data = response.json()

        if data.get("player"):
            for player in data["player"]:
                full_name = f"{player.get('strPlayer')}"
                if full_name:
                    all_players.append(full_name.strip())

    with open(output_path, "w", encoding="utf-8") as f:
        for name in sorted(set(all_players)):
            f.write(name + "\n")

    print(f"Saved {len(all_players)} NHL players to {output_path}")

if __name__ == "__main__":
    fetch_nhl_players()