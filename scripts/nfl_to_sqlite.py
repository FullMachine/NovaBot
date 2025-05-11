import os
import json
import sqlite3
from glob import glob

DB_FILE = 'nfl_stats.db'
DATA_DIR = 'data/nfl/player_logs'

# Connect to SQLite
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Create table (if not exists)
c.execute('''
CREATE TABLE IF NOT EXISTS game_logs (
    player TEXT,
    year INTEGER,
    game_date TEXT,
    opponent TEXT,
    result TEXT,
    week INTEGER,
    attempts INTEGER,
    yards INTEGER,
    average REAL,
    long INTEGER,
    touchdowns INTEGER,
    receptions INTEGER,
    fumbles INTEGER,
    fumbles_lost INTEGER,
    total_tackles INTEGER,
    solo_tackles INTEGER,
    assists INTEGER,
    sacks REAL,
    safeties INTEGER,
    passes_defended INTEGER,
    interceptions INTEGER,
    def_td INTEGER,
    forced_fumbles INTEGER,
    fumble_recoveries INTEGER,
    completions INTEGER,
    qb_rating REAL,
    games_started INTEGER,
    games_played INTEGER,
    scrape_datetime TEXT,
    source_url TEXT,
    scraper_version TEXT,
    verification_status TEXT
)
''')

# Load all JSON files
for player_dir in os.listdir(DATA_DIR):
    player_path = os.path.join(DATA_DIR, player_dir)
    if not os.path.isdir(player_path):
        continue
    for fname in os.listdir(player_path):
        if not fname.endswith('.json'):
            continue
        year = fname.replace('.json', '')
        fpath = os.path.join(player_path, fname)
        with open(fpath) as f:
            try:
                content = json.load(f)
                if 'data' in content and 'metadata' in content:
                    stats = content['data']
                    meta = content['metadata']
                else:
                    # fallback for old format
                    stats = content
                    meta = {}
            except Exception:
                continue
        for entry in stats:
            c.execute('''
                INSERT INTO game_logs (
                    player, year, game_date, opponent, result, week, attempts, yards, average, long, touchdowns, receptions, fumbles, fumbles_lost, total_tackles, solo_tackles, assists, sacks, safeties, passes_defended, interceptions, def_td, forced_fumbles, fumble_recoveries, completions, qb_rating, games_started, games_played, scrape_datetime, source_url, scraper_version, verification_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                player_dir,
                int(year) if year.isdigit() else None,
                entry.get('game_date'),
                entry.get('opponent'),
                entry.get('result'),
                entry.get('week'),
                entry.get('attempts'),
                entry.get('yards'),
                entry.get('average'),
                entry.get('long'),
                entry.get('touchdowns'),
                entry.get('receptions'),
                entry.get('fumbles'),
                entry.get('fumbles_lost'),
                entry.get('total_tackles'),
                entry.get('solo_tackles'),
                entry.get('assists'),
                entry.get('sacks'),
                entry.get('safeties'),
                entry.get('passes_defended'),
                entry.get('interceptions'),
                entry.get('def_td'),
                entry.get('forced_fumbles'),
                entry.get('fumble_recoveries'),
                entry.get('completions'),
                entry.get('qb_rating'),
                entry.get('games_started'),
                entry.get('games_played'),
                meta.get('scrape_datetime'),
                meta.get('source_url'),
                meta.get('scraper_version'),
                meta.get('verification_status')
            ))

conn.commit()
conn.close()
print('✅ All NFL player logs loaded into nfl_stats.db!') 