import requests
from bs4 import BeautifulSoup
import os

output_path = "players/nfl_players.txt"
teams = [
    "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
    "DAL", "DEN", "DET", "GB", "HOU", "IND", "JAX", "KC",
    "LV", "LAC", "LAR", "MIA", "MIN", "NE", "NO", "NYG",
    "NYJ", "PHI", "PIT", "SEA", "SF", "TB", "TEN", "WAS"
]

print("📥 Fetching active NFL rosters from FantasyPros...")
players = set()

for team in teams:
    url = f"https://www.fantasypros.com/nfl/depth-charts/{team.lower()}.php"
    print(f"🔎 Scraping {team} from {url}")
    
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        for link in soup.select("a.fp-player-link"):
            name = link.text.strip().lower().replace(" ", "-")
            if name:
                players.add(name)
    except Exception as e:
        print(f"⚠️ Failed {team}: {e}")

# Save to file
os.makedirs("players", exist_ok=True)
with open(output_path, "w") as f:
    for p in sorted(players):
        f.write(p + "\n")

print(f"✅ Saved {len(players)} players to {output_path}")