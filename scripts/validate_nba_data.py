import os
import json
from collections import defaultdict

DATA_DIR = 'data/nba/player_stats'
SEASONS = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]

missing_files = []
empty_files = []
broken_files = []
player_game_counts = defaultdict(dict)

print("\n=== NBA Data Health Check ===\n")
for season in SEASONS:
    season_dir = os.path.join(DATA_DIR, season)
    files = [f for f in os.listdir(season_dir) if f.endswith('.json')]
    print(f"Season {season}: {len(files)} player files found.")
    for fname in files:
        fpath = os.path.join(season_dir, fname)
        if not os.path.exists(fpath):
            missing_files.append(fpath)
            continue
        if os.path.getsize(fpath) == 0:
            empty_files.append(fpath)
            continue
        try:
            with open(fpath) as f:
                data = json.load(f)
            result_sets = data.get('resultSets') or data.get('resultsets')
            if not result_sets or not result_sets[0].get('rowSet'):
                broken_files.append(fpath)
                continue
            num_games = len(result_sets[0]['rowSet'])
            player_game_counts[season][fname] = num_games
        except Exception as e:
            broken_files.append(fpath)

print("\n=== Summary ===")
print(f"Missing files: {len(missing_files)}")
if missing_files:
    for f in missing_files:
        print(f"  MISSING: {f}")
print(f"Empty files: {len(empty_files)}")
if empty_files:
    for f in empty_files:
        print(f"  EMPTY: {f}")
print(f"Broken files: {len(broken_files)}")
if broken_files:
    for f in broken_files:
        print(f"  BROKEN: {f}")

print("\n=== Player Game Counts (sample) ===")
for season, players in player_game_counts.items():
    print(f"Season {season}:")
    for fname, num_games in list(players.items())[:5]:
        print(f"  {fname}: {num_games} games")
    if len(players) > 5:
        print(f"  ...and {len(players)-5} more players.")

print("\nHealth check complete.") 