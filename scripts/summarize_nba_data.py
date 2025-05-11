import os
import json
from collections import defaultdict

DATA_DIR = os.getenv("DATA_DIR", "data")
SEASON = "2022-23"  # Change this to the season you want to summarize
STATS_DIR = os.path.join(DATA_DIR, "nba", "player_stats", SEASON)

# Stats to summarize
STAT_KEYS = ["PTS", "AST", "REB", "STL", "BLK"]

leaderboard = defaultdict(lambda: {k: 0 for k in STAT_KEYS})

for filename in os.listdir(STATS_DIR):
    if not filename.endswith("_regular_season.json"):
        continue
    player_id = filename.split("_")[0]
    with open(os.path.join(STATS_DIR, filename), "r") as f:
        data = json.load(f)
    result_set = data.get("resultSets", [{}])[0]
    headers = result_set.get("headers", [])
    rows = result_set.get("rowSet", [])
    if not rows:
        continue
    # Find indices for stats
    idx = {k: headers.index(k) for k in STAT_KEYS if k in headers}
    # Sum up stats
    for row in rows:
        for k, i in idx.items():
            leaderboard[player_id][k] += row[i]

# Print leaderboard
print(f"NBA {SEASON} Player Stat Leaderboard:")
print(f"{'Player ID':<10}  " + "  ".join([f'{k:<5}' for k in STAT_KEYS]))
for player_id, stats in leaderboard.items():
    print(f"{player_id:<10}  " + "  ".join([f'{stats[k]:<5}' for k in STAT_KEYS])) 