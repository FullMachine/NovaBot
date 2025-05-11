from nba_api.stats.static import players
import time

# Get all players (past + present)
all_players = players.get_players()

# Save to players.txt
with open("players.txt", "w") as f:
    for player in all_players:
        name = player['full_name'].lower().strip()
        f.write(name + "\n")

print(f"✅ Exported {len(all_players)} player names to players.txt")