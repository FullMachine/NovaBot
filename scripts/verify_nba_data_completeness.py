import os
import json
from collections import defaultdict

DATA_DIR = 'data/nba/player_stats'
TYPES = ['regular_season', 'playoffs', 'preseason', 'playin']

def get_seasons():
    return sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])

def get_player_files(season):
    season_dir = os.path.join(DATA_DIR, season)
    return [f for f in os.listdir(season_dir) if f.endswith('.json')]

def main():
    seasons = get_seasons()
    print(f"\n=== NBA Data Completeness Report ===\n")
    all_stat_columns = set()
    issues = []
    for season in seasons:
        print(f"Season: {season}")
        season_dir = os.path.join(DATA_DIR, season)
        player_files = get_player_files(season)
        # Map: player_id -> {type: num_games}
        player_games = defaultdict(lambda: {t: 0 for t in TYPES})
        for fname in player_files:
            try:
                pid, typ = fname.replace('.json', '').split('_', 1)
                fpath = os.path.join(season_dir, fname)
                with open(fpath) as f:
                    data = json.load(f)
                result_sets = data.get('resultSets') or data.get('resultsets')
                if not result_sets or not result_sets[0].get('rowSet'):
                    issues.append(f"No data: {season}/{fname}")
                    continue
                rows = result_sets[0]['rowSet']
                player_games[pid][typ] = len(rows)
                # Collect stat columns
                for col in result_sets[0].get('headers', []):
                    all_stat_columns.add(col)
            except Exception as e:
                issues.append(f"Error reading {season}/{fname}: {e}")
        # Print summary for this season
        print(f"  Players found: {len(player_games)}")
        for typ in TYPES:
            count = sum(1 for g in player_games.values() if g[typ] > 0)
            print(f"    {typ}: {count} players with data")
        # Flag missing or zero-game players
        for pid, games in player_games.items():
            for typ in TYPES:
                if games[typ] == 0:
                    issues.append(f"Player {pid} missing or has 0 games for {typ} in {season}")
        print()
    print("=== Stat Columns Available ===")
    print(", ".join(sorted(all_stat_columns)))
    print("\n=== Issues Found ===")
    if not issues:
        print("No issues found! All players and games present for all types.")
    else:
        for issue in issues[:50]:
            print(issue)
        if len(issues) > 50:
            print(f"...and {len(issues)-50} more issues.")
    print("\nReport complete.")

if __name__ == "__main__":
    main() 