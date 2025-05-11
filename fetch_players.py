from nba_api.stats.static import players

# Get all players (past and current)
all_players = players.get_players()

# Filter only current active players
active_players = [p['full_name'] for p in all_players if p['is_active']]

# Sort alphabetically
active_players = sorted(active_players)

# Save to players.txt
with open("players.txt", "w") as f:
    for name in active_players:
        f.write(name + "\n")

print(f"{len(active_players)} players saved to players.txt")