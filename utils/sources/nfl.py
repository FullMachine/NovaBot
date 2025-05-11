import requests
import os

API_KEY = os.getenv("API_FOOTBALL_KEY")  # or hardcode for testing
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

def fetch_all_nfl_player_stats(season="2023"):
    league_id = 1  # NFL
    url = f"{BASE_URL}/players?league={league_id}&season={season}"
    players = []

    page = 1
    while True:
        print(f"Fetching page {page}")
        response = requests.get(f"{url}&page={page}", headers=HEADERS)
        data = response.json()

        if "response" not in data or not data["response"]:
            break

        for player_data in data["response"]:
            player_info = {
                "name": player_data["player"]["name"],
                "team": player_data["statistics"][0]["team"]["name"],
                "position": player_data["statistics"][0]["games"].get("position", "N/A"),
                "games_played": player_data["statistics"][0]["games"].get("appearences", 0),
                "touchdowns": player_data["statistics"][0]["touchdowns"].get("total", 0),
                "yards": player_data["statistics"][0]["yards"].get("total", 0),
            }
            players.append(player_info)

        if not data.get("paging") or data["paging"]["next"] is None:
            break

        page += 1

    return players