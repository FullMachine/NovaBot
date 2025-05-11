import os
import requests
from bs4 import BeautifulSoup
import string

def scrape_pfr_nfl_slugs():
    base_url = "https://www.pro-football-reference.com/players/"
    all_slugs = set()
    print("📥 Scraping NFL.com slugs from Pro Football Reference...")
    for letter in string.ascii_uppercase:
        url = f"{base_url}{letter}/"
        print(f"🌐 Visiting {url}")
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"❌ Failed to load {url}")
            continue
        soup = BeautifulSoup(resp.text, 'html.parser')
        table = soup.find('table', {'id': 'players'})
        if not table:
            print(f"⚠️ No player table found for {letter}")
            continue
        for row in table.find('tbody').find_all('tr'):
            nfl_link = row.find('a', href=True, text='NFL')
            if nfl_link:
                href = nfl_link['href']
                # Example: https://www.nfl.com/players/patrick-mahomes/
                parts = href.strip('/').split('/')
                if len(parts) >= 2 and parts[-2] == 'players':
                    slug = parts[-1]
                    all_slugs.add(slug)
        print(f"✅ Found {len(all_slugs)} unique slugs so far.")
    os.makedirs("players", exist_ok=True)
    with open("players/nfl_players.txt", "w") as f:
        for slug in sorted(all_slugs):
            f.write(slug + "\n")
    print(f"✅ Saved {len(all_slugs)} NFL.com slugs to players/nfl_players.txt")

if __name__ == "__main__":
    scrape_pfr_nfl_slugs() 