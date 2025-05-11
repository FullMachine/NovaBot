import json
import os
import requests
import time
from tqdm import tqdm

def decimal_minutes_to_mmss(decimal_minutes):
    if isinstance(decimal_minutes, str):
        try:
            decimal_minutes = float(decimal_minutes)
        except Exception:
            return decimal_minutes
    minutes = int(decimal_minutes)
    seconds = int(round((decimal_minutes - minutes) * 60))
    return f"{minutes}:{seconds:02d}"

DEFAULT_SEASON = '2023-24'
season = input(f"Enter season to verify (default {DEFAULT_SEASON}): ") or DEFAULT_SEASON
season_dir = f"data/nba/player_stats/{season}"

if not os.path.exists(season_dir):
    print(f"Season directory not found: {season_dir}")
    exit(1)

# Gather all player files first
player_files = [f for f in os.listdir(season_dir) if f.endswith('_regular_season.json')]

print(f"\nVerifying your data against NBA.com for {season} (all games, all players)...\n")

for filename in tqdm(player_files, desc="Players verified"):
    file_path = os.path.join(season_dir, filename)
    with open(file_path, 'r') as f:
        data = json.load(f)
    result_set = data['resultSets'][0]
    headers = result_set['headers']
    rows = result_set['rowSet']
    if not rows:
        continue
    player_name = rows[0][2]
    player_id = rows[0][1]
    all_match = True
    for row in rows:
        game_id = row[7]
        local_stats = {
            'MIN': row[headers.index('MIN')],
            'PTS': row[headers.index('PTS')],
            'REB': row[headers.index('REB')],
            'AST': row[headers.index('AST')],
        }
        url = f"https://stats.nba.com/stats/boxscoretraditionalv2?GameID={game_id}&StartPeriod=0&EndPeriod=0&RangeType=0&StartRange=0&EndRange=0"
        headers_api = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://www.nba.com/',
            'Origin': 'https://www.nba.com',
            'Accept': 'application/json, text/plain, */*',
        }
        try:
            resp = requests.get(url, headers=headers_api, timeout=10)
            resp.raise_for_status()
            boxscore = resp.json()
            player_stats_list = boxscore['resultSets'][0]['rowSet']
            player_headers = boxscore['resultSets'][0]['headers']
            found = False
            for stat_row in player_stats_list:
                if int(stat_row[player_headers.index('PLAYER_ID')]) == int(player_id):
                    found = True
                    nba_stats = {
                        'MIN': stat_row[player_headers.index('MIN')],
                        'PTS': stat_row[player_headers.index('PTS')],
                        'REB': stat_row[player_headers.index('REB')],
                        'AST': stat_row[player_headers.index('AST')],
                    }
                    mismatches = []
                    local_min = decimal_minutes_to_mmss(local_stats['MIN'])
                    if local_min != nba_stats['MIN']:
                        mismatches.append(f"MIN: local {local_min} vs NBA.com {nba_stats['MIN']}")
                    for stat in ['PTS', 'REB', 'AST']:
                        if str(local_stats[stat]) != str(nba_stats[stat]):
                            mismatches.append(f"{stat}: local {local_stats[stat]} vs NBA.com {nba_stats[stat]}")
                    if mismatches:
                        print(f"Mismatch for {player_name} ({game_id}):")
                        for m in mismatches:
                            print(f"  - {m}")
                        all_match = False
                    break
            if not found:
                print(f"{player_name:20} | {game_id} | Player not found in NBA stats API.")
                all_match = False
        except Exception as e:
            print(f"Error checking {player_name} ({game_id}): {e}")
            all_match = False
        time.sleep(0.5)  # Be polite to NBA.com
    if all_match:
        print(f"{player_name:20} | All games match!")

print("\nVerification complete. Checked all games for all players.") 