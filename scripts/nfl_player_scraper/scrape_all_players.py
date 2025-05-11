import os
from time import sleep
from scrape_player_stats import scrape_player_stats

# File with player slugs (e.g. tua-tagovailoa, patrick-mahomes)
with open("players/nfl_players.txt") as f:
    player_names = [line.strip() for line in f.readlines() if line.strip()]

# Folder and years
base_dir = "data/nfl/player_stats"
years = [2020, 2021, 2022, 2023]

# Loop through all players and scrape each year
for player in player_names:
    print(f"\n📊 Scraping {player}...")

    player_folder = os.path.join(base_dir, player)
    os.makedirs(player_folder, exist_ok=True)

    for year in years:
        output_path = os.path.join(player_folder, f"{year}.json")

        if os.path.exists(output_path):
            print(f"✅ Already exists: {player} {year}")
            continue

        try:
            scrape_player_stats(player, year)
            sleep(1)
        except Exception as e:
            print(f"❌ Failed {player} {year}: {e}")