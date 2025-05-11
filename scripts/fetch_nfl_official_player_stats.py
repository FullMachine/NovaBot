import os
import json
import time
import requests
from tqdm import tqdm

DATA_DIR = 'data/nfl/player_stats'
SEASONS = ['2020', '2021', '2022', '2023']
NFL_API_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/statistics'
NFL_PLAYERS_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/players'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

def fetch_players(season):
    # ESPN API paginates players, so we loop through pages
    players = []
    page = 1
    while True:
        params = {'season': season, 'page': page}
        resp = requests.get(NFL_PLAYERS_URL, headers=HEADERS, params=params, timeout=10)
        if resp.status_code != 200:
            break
        data = resp.json()
        items = data.get('athletes', [])
        if not items:
            break
        for item in items:
            player = item.get('athlete') or item
            if player:
                players.append({
                    'id': player.get('id'),
                    'name': player.get('displayName'),
                    'slug': player.get('slug'),
                })
        page += 1
        time.sleep(0.5)
    return players

def fetch_player_stats(player_id, season):
    params = {'season': season, 'athlete': player_id}
    resp = requests.get(NFL_API_URL, headers=HEADERS, params=params, timeout=10)
    if resp.status_code != 200:
        return None
    return resp.json()

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    for season in SEASONS:
        print(f'\n=== {season} ===')
        players = fetch_players(season)
        print(f'Total players: {len(players)}')
        for player in tqdm(players, desc=f'Players in {season}'):
            player_name = player['slug'] or player['name'].replace(' ', '-').lower()
            player_dir = os.path.join(DATA_DIR, player_name)
            ensure_dir(player_dir)
            fpath = os.path.join(player_dir, f'{season}.json')
            if os.path.exists(fpath):
                continue
            stats = fetch_player_stats(player['id'], season)
            if stats:
                with open(fpath, 'w') as f:
                    json.dump(stats, f)
                tqdm.write(f'Saved stats for {player["name"]} ({season})')
            else:
                tqdm.write(f'No stats for {player["name"]} ({season})')
            time.sleep(1)
    print('Done!')

if __name__ == '__main__':
    main() 