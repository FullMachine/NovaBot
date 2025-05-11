import os
import json

player_dir = "data/nfl/player_stats"
player_file = "players/nfl_players.txt"

def has_valid_stats(player):
    player_path = os.path.join(player_dir, player)
    if not os.path.isdir(player_path):
        return False

    for file in os.listdir(player_path):
        if file.endswith(".json"):
            try:
                with open(os.path.join(player_path, file)) as f:
                    data = json.load(f)
                    if isinstance(data, list) and len(data) > 0:
                        return True
            except:
                continue
    return False

with open(player_file) as f:
    players = [line.strip() for line in f if line.strip()]

valid_players = []

for player in players:
    if has_valid_stats(player):
        valid_players.append(player)
    else:
        print(f"🗑 Removing {player} (no stats)")

with open(player_file, "w") as f:
    for player in valid_players:
        f.write(player + "\n")

print(f"\n✅ Cleaned! Kept {len(valid_players)} valid players.")