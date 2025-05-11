import os
import json
import time
import requests
from tqdm import tqdm

DATA_DIR = 'data/nba/player_stats'
SEASONS = ['2020-21', '2021-22', '2022-23', '2023-24']
GAME_TYPES = [
    ('Regular Season', 'regular_season'),
    ('Playoffs', 'playoffs'),
    ('Pre Season', 'preseason'),
    ('PlayIn', 'playin'),
]
NBA_PLAYER_GAMELOGS_URL = 'https://stats.nba.com/stats/playergamelogs'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://www.nba.com/players',
    'Origin': 'https://www.nba.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

ERROR_LOG = 'nba_scraper_errors.log'

def get_active_players(season, season_type):
    params = {
        'Season': season,
        'SeasonType': season_type,
        'LeagueID': '00',
        'PlayerOrTeam': 'P',
    }
    try:
        resp = requests.get(NBA_PLAYER_GAMELOGS_URL, headers=HEADERS, params=params, timeout=10)
        if resp.status_code == 429:
            print('Rate limited. Sleeping for 30 seconds...')
            time.sleep(30)
            resp = requests.get(NBA_PLAYER_GAMELOGS_URL, headers=HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        headers_ = data['resultSets'][0]['headers']
        rows = data['resultSets'][0]['rowSet']
        player_id_idx = headers_.index('PLAYER_ID')
        player_name_idx = headers_.index('PLAYER_NAME')
        players = {}
        for row in rows:
            pid = row[player_id_idx]
            pname = row[player_name_idx]
            players[pid] = pname
        return players
    except Exception as e:
        print(f'  ✖ Error fetching active players for {season} {season_type}: {e}')
        with open(ERROR_LOG, 'a') as log:
            log.write(f'Error fetching active players for {season} {season_type}: {e}\n')
        return {}

def fetch_player_gamelogs(player_id, season, season_type):
    params = {
        'PlayerID': player_id,
        'Season': season,
        'SeasonType': season_type,
        'LeagueID': '00',
    }
    for attempt in range(3):
        try:
            resp = requests.get(NBA_PLAYER_GAMELOGS_URL, headers=HEADERS, params=params, timeout=10)
            if resp.status_code == 429:
                print('Rate limited. Sleeping for 30 seconds...')
                time.sleep(30)
                continue
            resp.raise_for_status()
            data = resp.json()
            # Validate data
            result_sets = data.get('resultSets') or data.get('resultsets')
            if not result_sets or not result_sets[0].get('rowSet'):
                print(f'  ⚠ No valid data for {player_id} {season} {season_type} (attempt {attempt+1})')
                time.sleep(2)
                continue
            return data
        except Exception as e:
            print(f'  ✖ Error fetching gamelogs for {player_id} {season} {season_type} (attempt {attempt+1}): {e}')
            time.sleep(2)
    # Log failed attempts
    with open(ERROR_LOG, 'a') as log:
        log.write(f'Failed to fetch gamelogs for {player_id} {season} {season_type} after 3 attempts\n')
    return None

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def is_data_valid(data):
    try:
        result_sets = data.get('resultSets') or data.get('resultsets')
        if not result_sets:
            return False
        rows = result_sets[0].get('rowSet', [])
        return bool(rows)
    except Exception:
        return False

def main():
    for season in SEASONS:
        print(f'\n=== {season} ===')
        season_dir = os.path.join(DATA_DIR, season)
        ensure_dir(season_dir)
        fetched = 0
        empty = 0
        for nba_type, file_type in GAME_TYPES:
            print(f'Getting active players for {season} {nba_type}...')
            players = get_active_players(season, nba_type)
            if not players:
                print(f'Skipping {season} {nba_type} due to error or no players.')
                continue
            print(f'Total active players: {len(players)}')
            with tqdm(total=len(players), desc=f"Players in {season} {nba_type}") as pbar:
                for pid, pname in players.items():
                    fname = f'{pid}_{file_type}.json'
                    fpath = os.path.join(season_dir, fname)
                    # Skip if file exists and is valid
                    if os.path.exists(fpath):
                        try:
                            with open(fpath) as f:
                                data = json.load(f)
                            if is_data_valid(data):
                                pbar.update(1)
                                continue
                        except Exception:
                            pass
                    try:
                        tqdm.write(f'Fetching {nba_type} for {pname} ({pid})...')
                        data = fetch_player_gamelogs(pid, season, nba_type)
                        if data and is_data_valid(data):
                            with open(fpath, 'w') as f:
                                json.dump(data, f)
                            tqdm.write(f'  ✔ Data collected for {nba_type} ({len(data["resultSets"][0]["rowSet"])} games)')
                            fetched += 1
                        else:
                            tqdm.write(f'  ⚠ No valid data for {nba_type} {pname} ({pid})')
                            empty += 1
                        time.sleep(1.5)
                    except Exception as e:
                        tqdm.write(f'  ✖ Error fetching {nba_type} for {pname} ({pid}): {e}')
                        with open(ERROR_LOG, 'a') as log:
                            log.write(f'Error fetching {nba_type} for {pname} ({pid}): {e}\n')
                        continue
                    pbar.update(1)
        print(f'Finished {season}: {fetched} files with data, {empty} empty or invalid files.')

if __name__ == '__main__':
    main() 