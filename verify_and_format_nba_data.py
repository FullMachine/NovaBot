import json
import os

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

print(f"\nVerifying and formatting minutes for all players in {season}...\n")

for filename in os.listdir(season_dir):
    if filename.endswith('_regular_season.json'):
        file_path = os.path.join(season_dir, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)
        result_set = data['resultSets'][0]
        headers = result_set['headers']
        rows = result_set['rowSet']
        if not rows:
            continue
        min_idx = headers.index('MIN')
        player_name = rows[0][2]
        # Convert all MIN values to MM:SS format
        for row in rows:
            row[min_idx] = decimal_minutes_to_mmss(row[min_idx])
        # Print summary for the first game
        print(f"Player: {player_name:20} | First Game: {rows[0][8]} | MIN: {rows[0][min_idx]}")
        # Save the updated file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

print("\nAll player files checked and updated. Minutes are now in MM:SS format.") 