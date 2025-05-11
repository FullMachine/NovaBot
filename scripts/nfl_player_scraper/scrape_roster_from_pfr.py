import os
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.pro-football-reference.com/players"
output_file = "players/nfl_players.txt"
os.makedirs("players", exist_ok=True)

def scrape_all_players():
    all_players = set()

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(f"🔤 Scraping letter {letter}...")
        url = f"{BASE_URL}/{letter}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        players_table = soup.find("div", {"id": "div_players"})

        if players_table:
            for link in players_table.find_all("a"):
                name = link.text.strip()
                href = link.get("href")
                if name and "/players/" in href:
                    slug = name.lower().replace(".", "").replace("'", "").replace(" ", "-")
                    all_players.add(slug)
        else:
            print(f"❌ Could not find player list on page {url}")

    with open(output_file, "w") as f:
        for player in sorted(all_players):
            f.write(player + "\n")

    print(f"\n✅ Saved {len(all_players)} players to {output_file}")

if __name__ == "__main__":
    scrape_all_players()