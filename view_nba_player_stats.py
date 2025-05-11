import json
import os
from tabulate import tabulate

# Default values for quick testing
DEFAULT_PLAYER_NAME = 'Zach Collins'
DEFAULT_SEASON = '2023-24'

# Ask user for player name and season (or use default)
player_name = input(f"Enter NBA Player Name (default {DEFAULT_PLAYER_NAME}): ") or DEFAULT_PLAYER_NAME
season = input(f"Enter season (default {DEFAULT_SEASON}): ") or DEFAULT_SEASON

# Build directory path
season_dir = f"data/nba/player_stats/{season}"

if not os.path.exists(season_dir):
    print(f"Season directory not found: {season_dir}")
    print("Make sure the season is correct.")
    exit(1)

# Find the file for the player name
player_file = None
for filename in os.listdir(season_dir):
    if filename.endswith('_regular_season.json'):
        file_path = os.path.join(season_dir, filename)
        with open(file_path, 'r') as f:
            data = json.load(f)
            result_set = data['resultSets'][0]
            if result_set['rowSet']:
                # Get the player name from the first game
                name_in_file = result_set['rowSet'][0][2].lower()
                if player_name.lower() == name_in_file:
                    player_file = file_path
                    break

if not player_file:
    print(f"Player '{player_name}' not found in season {season}.")
    exit(1)

# Load the JSON data
with open(player_file, 'r') as f:
    data = json.load(f)

# Extract headers and rows
result_set = data['resultSets'][0]
headers = result_set['headers']
rows = result_set['rowSet']

# Print a table of all games
print(f"\nShowing stats for {player_name} in {season} (all games):\n")
print(tabulate(rows, headers=headers, tablefmt="grid"))

print("\nTo check another player or season, just run this script again!") 