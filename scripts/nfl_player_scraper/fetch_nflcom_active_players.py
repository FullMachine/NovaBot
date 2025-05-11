import requests
from bs4 import BeautifulSoup
import os

TEAM_CODES = [
    "ari", "atl", "bal", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gb",
    "hou", "ind", "jax", "kc", "lv", "lac", "lar", "mia", "min", "ne", "no", "nyg",
    "nyj", "phi", "pit", "sf", "sea", "tb", "ten", "wsh"
]

output_path = "players/nfl_players.txt"
all_players = []

print("📡 Fetching active NFL rosters from NFL.com...")

for team in TEAM_CODES:
    url = f"https://www.nfl.com/teams/{team}/roster"
    print(f"🔍 Scraping: {url}")
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table")
        if not table:
            print(f"⚠️ No table found for {team}")
            continue
        rows = table.find_all("tr")[1:]  # skip header row
        for row in rows:
            name_cell = row.find("a")
            if name_cell:
                name = name_cell.text.strip().lower().replace(" ", "-")
                if name not in all_players:
                    all_players.append(name)
    except Exception as e:
        print(f"❌ Error on {team}: {e}")

# Save to file
os.makedirs("players", exist_ok=True)
with open(output_path, "w") as f:
    for name in sorted(all_players):
        f.write(name + "\n")

print(f"✅ Saved {len(all_players)} active players to {output_path}")