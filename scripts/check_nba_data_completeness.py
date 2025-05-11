import os
import json
import requests
from collections import defaultdict

# Helper: Get all season folders
DATA_DIR = 'data/nba/player_stats'
SEASONS = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]

# Helper: Get all local player files for a season
def get_local_player_files(season):
    season_dir = os.path.join(DATA_DIR, season)
    files = os.listdir(season_dir)
    player_files = defaultdict(dict)
    for f in files:
        if f.endswith('.json'):
            parts = f.split('_')
            if len(parts) == 3:
                player_id, game_type, _ = parts
                player_files[player_id][game_type] = f
    return player_files

# Helper: Get official player list for a season (regular season only, for now)
def get_official_players_bref(season):
    # Basketball Reference season format: 2024 for 2023-24
    year = int(season.split('-')[1])
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html'
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Failed to fetch Basketball Reference for {season}")
        return set()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table', {'id': 'per_game_stats'})
    players = set()
    if table:
        for row in table.tbody.find_all('tr'):
            if row.get('class') and 'thead' in row.get('class'):
                continue
            player = row.find('td', {'data-stat': 'player'})
            if player:
                players.add(player.text.strip())
    return players

# Main completeness check
def check_completeness():
    for season in sorted(SEASONS):
        print(f'\n=== {season} ===')
        local_files = get_local_player_files(season)
        official_players = get_official_players_bref(season)
        local_names = set()
        # Try to map player_id to name from local files
        for player_id, files in local_files.items():
            for game_type, fname in files.items():
                path = os.path.join(DATA_DIR, season, fname)
                try:
                    with open(path) as f:
                        data = json.load(f)
                        # Try to get player name from data
                        if 'resultSets' in data and data['resultSets']:
                            rows = data['resultSets'][0].get('rowSet', [])
                            if rows:
                                local_names.add(rows[0][2])
                except Exception as e:
                    continue
        missing_players = official_players - local_names
        print(f"Players in official stats: {len(official_players)}")
        print(f"Players with local data: {len(local_names)}")
        print(f"Missing players: {len(missing_players)}")
        if missing_players:
            print("Sample missing:", list(missing_players)[:10])
        # Check for missing game types
        for player_id, files in local_files.items():
            for game_type in ['regular', 'playoffs', 'preseason', 'playin']:
                if game_type not in files:
                    print(f"Player {player_id} missing {game_type} data in {season}")
                else:
                    # Check if file is empty
                    path = os.path.join(DATA_DIR, season, files[game_type])
                    try:
                        with open(path) as f:
                            data = json.load(f)
                            if not data.get('resultSets') or not data['resultSets'][0].get('rowSet'):
                                print(f"Player {player_id} {game_type} file is empty in {season}")
                    except Exception as e:
                        print(f"Error reading {path}: {e}")

if __name__ == '__main__':
    check_completeness() 