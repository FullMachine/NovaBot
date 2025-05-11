import os
import json
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

def scrape_player_stats(player_slug, year):
    print(f"📥 Scraping stats for {player_slug} in {year}...")

    url = f"https://www.nfl.com/players/{player_slug}/stats/logs/{year}/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {url}")

    soup = BeautifulSoup(response.text, "html.parser")

    # All sections for game logs (e.g. Preseason, Regular Season, Postseason)
    tables = soup.find_all("table", class_="d3-o-table")

    all_stats = []

    for table in tables:
        section = table.find_previous("h3")
        section_title = section.text.strip() if section else "Unknown"

        headers = [th.text.strip() for th in table.find_all("th")]

        for row in table.find("tbody").find_all("tr"):
            cells = row.find_all("td")
            if not cells or len(cells) != len(headers):
                continue  # skip header/subtotal rows

            game_data = {
                "section": section_title,
                "player": player_slug,
                "year": year
            }

            for idx, cell in enumerate(cells):
                game_data[headers[idx]] = unidecode(cell.text.strip())

            all_stats.append(game_data)

    if not all_stats:
        print(f"⚠️ No data found for {player_slug} {year}")
        return

    # Save to file
    save_path = os.path.join("data", "nfl", "player_stats", player_slug, f"{year}.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w") as f:
        json.dump(all_stats, f, indent=2)

    print(f"✅ Saved {len(all_stats)} games to {save_path}")