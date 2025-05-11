import os
import pandas as pd

DATA_DIR = "nflfastR-data/data/roster"
YEARS = [2023, 2022, 2021]  # you can add more years if needed

players = set()

for year in YEARS:
    file_path = os.path.join(DATA_DIR, f"roster_{year}.csv")
    if not os.path.exists(file_path):
        print(f"File not found for {year}: {file_path}")
        continue

    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        name = row.get("full_name") or row.get("name")
        team = row.get("team", "")
        position = row.get("position", "")
        if pd.notnull(name):
            players.add(f"{name} - {team} - {position}")

# Save to file
with open("players/nfl_players.txt", "w") as f:
    for player in sorted(players):
        f.write(player + "\n")

print(f"✅ Saved {len(players)} NFL players from nflfastR-data to players/nfl_players.txt")