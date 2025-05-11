import requests
import json

# NBA.com API endpoint for all players in a season (2023-24)
# We'll use the "commonallplayers" endpoint to get all players for a given season
SEASON = '2023-24'

# NBA.com API endpoint for all game logs (player-level)
API_URL = 'https://stats.nba.com/stats/commonallplayers'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://www.nba.com/players',
    'Origin': 'https://www.nba.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

def fetch_all_players(season):
    params = {
        'IsOnlyCurrentSeason': '0',
        'LeagueID': '00',
        'Season': season,
    }
    resp = requests.get(API_URL, headers=HEADERS, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']
    player_id_idx = headers.index('PERSON_ID')
    player_name_idx = headers.index('DISPLAY_FIRST_LAST')
    players = {}
    for row in rows:
        pid = row[player_id_idx]
        pname = row[player_name_idx]
        players[pid] = pname
    return players

def main():
    print(f'Fetching all players for {SEASON}...')
    players = fetch_all_players(SEASON)
    print(f"Total players in {SEASON}: {len(players)}")
    print("Sample:", list(players.items())[:10])
    with open(f'players_{SEASON.replace("-", "_")}_nba_official.json', 'w') as f:
        json.dump(players, f, indent=2)
    print(f"Saved to players_{SEASON.replace('-', '_')}_nba_official.json")

if __name__ == '__main__':
    main() 