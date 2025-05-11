import os
import time
import json
import requests
from tqdm import tqdm
from vision_scraper import scrape_nfl_stats_for_url, save_stats, extract_player_slug
from utils.helpers import get_active_years_for_player
import datetime
import pickle
import logging

# ESPN API setup
NFL_API_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/statistics'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

def fetch_espn_stats(player_id, season):
    params = {'season': season, 'athlete': player_id}
    try:
        resp = requests.get(NFL_API_URL, headers=HEADERS, params=params, timeout=10)
        if resp.status_code != 200:
            return None
        return resp.json()
    except Exception:
        return None

# Load player slugs from text file
with open("players/nfl_players.txt", "r") as f:
    player_slugs = [line.strip() for line in f if line.strip()]

# For progress tracking
summary = {
    'successful': [],
    'skipped': [],
    'fallback_used': [],
    'errors': [],
    'empty_files': [],
    'verified': [],
    'mismatched': [],
    'missing_years': [],
    'incomplete_files': [],
    'suspicious_files': [],
    'missing_columns': []
}
total_players = len(player_slugs)

# Load ESPN player slug->id mapping (build once for all seasons)
espn_slug_to_id = {}
for season in ['2023']:
    # Only need one season for mapping, as IDs are stable
    url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/players'
    page = 1
    while True:
        params = {'season': season, 'page': page}
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if resp.status_code != 200:
            break
        data = resp.json()
        items = data.get('athletes', [])
        if not items:
            break
        for item in items:
            player = item.get('athlete') or item
            if player and player.get('slug'):
                espn_slug_to_id[player['slug']] = player['id']
        page += 1
        time.sleep(0.5)

# Determine the range of years to scrape
start_year = 2016
current_year = datetime.datetime.now().year
all_years = list(range(start_year, current_year + 1))

PROGRESS_FILE = 'nfl_scraper_progress.pkl'

# Load progress if exists
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'rb') as pf:
        completed = pickle.load(pf)
else:
    completed = set()

# Set up logging
logging.basicConfig(
    filename='nfl_scraper.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

# Loop through each player
for player_slug in tqdm(player_slugs, desc="📊 Players Scraped"):
    full_name = player_slug.replace("-", " ").title()
    try:
        for year in all_years:
            progress_key = f"{player_slug}:{year}"
            if progress_key in completed:
                continue  # Already done
            url = f"https://www.nfl.com/players/{player_slug}/stats/logs/{year}/"
            for attempt in range(3):
                try:
                    stats_by_section = scrape_nfl_stats_for_url(url)
                    if stats_by_section:
                        save_stats(stats_by_section, player_slug, year, source_url=url)
                        summary['successful'].append({'player': full_name, 'year': year})
                        logging.info(f"SUCCESS: {full_name} {year}")
                        espn_id = espn_slug_to_id.get(player_slug)
                        if espn_id:
                            espn_stats = fetch_espn_stats(espn_id, year)
                            if espn_stats and str(stats_by_section) == str(espn_stats):
                                summary['verified'].append({'player': full_name, 'year': year})
                                logging.info(f"VERIFIED: {full_name} {year}")
                            else:
                                summary['mismatched'].append({'player': full_name, 'year': year})
                                logging.warning(f"MISMATCH: {full_name} {year}")
                        completed.add(progress_key)
                        with open(PROGRESS_FILE, 'wb') as pf:
                            pickle.dump(completed, pf)
                        break
                    else:
                        print(f"🚫 No data for {full_name} in {year}")
                        summary['missing_years'].append({'player': full_name, 'year': year, 'reason': 'No data'})
                        logging.warning(f"NO DATA: {full_name} {year}")
                        break
                except Exception as e:
                    print(f"❌ Error for {full_name} in {year} (attempt {attempt+1}): {e}")
                    logging.error(f"ERROR: {full_name} {year} (attempt {attempt+1}): {e}")
                    if attempt == 2:
                        summary['errors'].append({'player': full_name, 'year': year, 'error': str(e)})
                        logging.error(f"FAILED: {full_name} {year} after 3 attempts")
            time.sleep(1)
    except Exception as e:
        print(f"❌ Error for {full_name}: {e}")
        summary['errors'].append({'player': full_name, 'error': str(e)})
        logging.error(f"FATAL ERROR: {full_name}: {e}")
        continue

# Check for empty/invalid files
player_stats_dir = "data/nfl/player_stats"
for player in os.listdir(player_stats_dir):
    player_dir = os.path.join(player_stats_dir, player)
    if os.path.isdir(player_dir):
        for fname in os.listdir(player_dir):
            fpath = os.path.join(player_dir, fname)
            try:
                if os.path.getsize(fpath) == 0:
                    summary['empty_files'].append(fpath)
                    continue
                with open(fpath) as f:
                    data = json.load(f)
                if not data or not isinstance(data, list):
                    summary['incomplete_files'].append(fpath)
                    continue
                # Check for missing columns
                for entry in data:
                    missing = [col for col in EXPECTED_COLUMNS if col not in entry]
                    if missing:
                        summary['missing_columns'].append({'file': fpath, 'missing': missing})
                # Check for suspicious stats (all zeros or empty)
                for entry in data:
                    values = list(entry.values())
                    if all(v == '' or v == '0' for v in values if isinstance(v, str)):
                        summary['suspicious_files'].append({'file': fpath, 'entry': entry})
            except Exception:
                summary['incomplete_files'].append(fpath)

# Cross-verification after scraping
for player in os.listdir(player_stats_dir):
    player_dir = os.path.join(player_stats_dir, player)
    if os.path.isdir(player_dir):
        for fname in os.listdir(player_dir):
            fpath = os.path.join(player_dir, fname)
            try:
                with open(fpath) as f:
                    nfl_data = json.load(f)
                # Extract year from filename
                year = fname.replace('.json', '')
                espn_id = espn_slug_to_id.get(player)
                if espn_id:
                    espn_stats = fetch_espn_stats(espn_id, year)
                    if espn_stats and isinstance(nfl_data, list) and len(nfl_data) > 0:
                        # Simple comparison: check if number of games matches
                        nfl_games = len(nfl_data)
                        espn_games = 0
                        # ESPN data structure may vary; try to count games
                        if 'athletes' in espn_stats and espn_stats['athletes']:
                            stats = espn_stats['athletes'][0].get('stats', [])
                            if isinstance(stats, list):
                                espn_games = len(stats)
                        if nfl_games == espn_games:
                            summary['verified'].append({'file': fpath, 'nfl_games': nfl_games, 'espn_games': espn_games})
                        else:
                            summary['mismatched'].append({'file': fpath, 'nfl_games': nfl_games, 'espn_games': espn_games})
            except Exception:
                continue

# Save summary report
with open("nfl_scraper_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# At the end, print a summary to the console
print("\n===== NFL Scraper Run Summary =====")
print(f"Total Players: {len(player_slugs)}")
print(f"Successful: {len(summary['successful'])}")
print(f"Verified: {len(summary['verified'])}")
print(f"Mismatched: {len(summary['mismatched'])}")
print(f"Missing Years: {len(summary['missing_years'])}")
print(f"Incomplete Files: {len(summary['incomplete_files'])}")
print(f"Suspicious Files: {len(summary['suspicious_files'])}")
print(f"Missing Columns: {len(summary['missing_columns'])}")
print(f"Errors: {len(summary['errors'])}")
print(f"Empty/Invalid Files: {len(summary['empty_files'])}")
print(f"See nfl_scraper_summary.json and nfl_scraper.log for details.")
