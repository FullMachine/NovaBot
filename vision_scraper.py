import os
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime

# Set up Chrome WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Explicitly set the path to ChromeDriver installed by Homebrew
    chromedriver_path = "/opt/homebrew/bin/chromedriver"
    if not os.path.exists(chromedriver_path):
        # Fallback for Intel Macs or alternative installations
        chromedriver_path = "/usr/local/bin/chromedriver"
        if not os.path.exists(chromedriver_path):
            raise FileNotFoundError("ChromeDriver not found at /opt/homebrew/bin/chromedriver or /usr/local/bin/chromedriver. Please install or check path.")

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Parse NFL stats from a given URL
def scrape_nfl_stats_for_url(url):
    print(f"🌐 Visiting {url}")
    driver = setup_driver()
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Updated selector for the stats table
    table = soup.select_one("table.d3-o-table")
    if not table:
        print("❌ No stat tables found.")
        return []

    all_stats = []
    rows = table.find_all("tr")
    if not rows or len(rows) < 2:
        print("❌ No data rows found in table.")
        return []

    headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]
    print(f"📋 Columns: {headers}")

    for row in rows[1:]:
        cells = row.find_all("td")
        cols = [td.get_text(strip=True) for td in cells]
        if not cols or all(c == '' for c in cols):
            continue
        # Dynamically map columns to headers
        game_log = dict(zip(headers, cols))
        # Log missing columns
        missing = [h for h in headers if h not in game_log or game_log[h] == '']
        if missing:
            print(f"⚠️ Missing/empty columns for row: {missing}")
        all_stats.append(game_log)

    return all_stats

def normalize_stats(stats):
    # Standardize field names
    field_map = {
        'Game Date': 'game_date',
        'OPP': 'opponent',
        'RESULT': 'result',
        'WK': 'week',
        'ATT': 'attempts',
        'YDS': 'yards',
        'AVG': 'average',
        'LNG': 'long',
        'TD': 'touchdowns',
        'REC': 'receptions',
        'FUM': 'fumbles',
        'LOST': 'fumbles_lost',
        'Total': 'total_tackles',
        'Solo': 'solo_tackles',
        'AST': 'assists',
        'SCK': 'sacks',
        'SFTY': 'safeties',
        'PDEF': 'passes_defended',
        'INT': 'interceptions',
        'TDS': 'def_td',
        'FF': 'forced_fumbles',
        'FR': 'fumble_recoveries',
        'COMP': 'completions',
        'RATE': 'qb_rating',
        'GS': 'games_started',
        'G': 'games_played',
    }
    normalized = []
    for entry in stats:
        norm_entry = {}
        for k, v in entry.items():
            key = field_map.get(k, k.lower().replace(' ', '_'))
            # Normalize team names (remove @ for away, keep as string)
            if key == 'opponent' and v.startswith('@'):
                v = v[1:]
            # Normalize date to YYYY-MM-DD
            if key == 'game_date':
                try:
                    v = re.sub(r'(\d{2})/(\d{2})/(\d{4})', r'\3-\1-\2', v)
                except Exception:
                    pass
            norm_entry[key] = v
        normalized.append(norm_entry)
    return normalized

# Save stats to file
def save_stats(stats, player_slug, year, source_url=None, verification_status=None):
    stats = normalize_stats(stats)
    save_path = f"data/nfl/player_logs/{player_slug}"
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, f"{year}.json")
    metadata = {
        'scrape_datetime': datetime.now().isoformat(),
        'source_url': source_url or f"https://www.nfl.com/players/{player_slug}/stats/logs/{year}/",
        'scraper_version': '1.0',
        'verification_status': verification_status or 'unverified'
    }
    output = {
        'metadata': metadata,
        'data': stats
    }
    with open(file_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"✅ Saved {len(stats)} entries to {file_path}")

# Extract player slug from a full URL
def extract_player_slug(url):
    try:
        parts = url.strip("/").split("/")
        if "players" in parts:
            idx = parts.index("players")
            return parts[idx + 1]
        return None
    except Exception as e:
        print(f"❌ Failed to extract slug from URL: {e}")
        return None

# Manual entry point
if __name__ == "__main__":
    url = input("Enter full NFL stats URL (e.g. https://www.nfl.com/players/patrick-mahomes/stats/logs/2022/): ").strip()
    stats = scrape_nfl_stats_for_url(url)
    if stats:
        slug = extract_player_slug(url)
        year = url.rstrip("/").split("/")[-1]
        save_stats(stats, slug, year)
