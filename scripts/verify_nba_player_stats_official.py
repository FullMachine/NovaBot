import os
import json
import csv
import aiohttp
import asyncio
from typing import Dict, List

NBA_PLAYER_GAMELOG_URL = "https://stats.nba.com/stats/playergamelogs?PlayerID={player_id}&Season={season}&SeasonType={season_type}"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.nba.com',
    'Accept': 'application/json'
}

PLAYER_STATS_DIR = "data/nba/player_stats"
OUTPUT_FILE = "verify_nba_player_stats_full_report.csv"
REQUEST_DELAY = 0.5  # seconds

async def fetch_official_gamelogs(session, player_id: str, season: str, season_type: str) -> Dict[str, Dict]:
    url = NBA_PLAYER_GAMELOG_URL.format(player_id=player_id, season=season, season_type=season_type)
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            sets = data.get('resultSets', [])
            if sets and sets[0]['rowSet']:
                headers = sets[0]['headers']
                return {row[7]: dict(zip(headers, row)) for row in sets[0]['rowSet']}  # GAME_ID as key
        return {}

def compare_gamelogs(local_games: Dict[str, Dict], official_games: Dict[str, Dict]) -> List[Dict]:
    discrepancies = []
    all_game_ids = set(local_games.keys()) | set(official_games.keys())
    for game_id in all_game_ids:
        local = local_games.get(game_id)
        official = official_games.get(game_id)
        if not local:
            discrepancies.append({'GAME_ID': game_id, 'Type': 'Missing in Local', 'Details': official})
        elif not official:
            discrepancies.append({'GAME_ID': game_id, 'Type': 'Missing in Official', 'Details': local})
        else:
            for key in official:
                local_val = local.get(key)
                official_val = official.get(key)
                if str(local_val) != str(official_val):
                    discrepancies.append({'GAME_ID': game_id, 'Type': 'Mismatch', 'Field': key, 'Local': local_val, 'Official': official_val})
    return discrepancies

async def main():
    results = []
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for season in os.listdir(PLAYER_STATS_DIR):
            season_dir = os.path.join(PLAYER_STATS_DIR, season)
            if not os.path.isdir(season_dir):
                continue
            for fname in os.listdir(season_dir):
                if not fname.endswith('.json'):
                    continue
                player_id = fname.split('_')[0]
                season_type = 'Regular Season' if 'regular_season' in fname else 'Playoffs'
                with open(os.path.join(season_dir, fname), 'r') as f:
                    local_data = json.load(f)
                sets = local_data.get('resultSets', [])
                if not sets or not sets[0]['rowSet']:
                    continue
                headers = sets[0]['headers']
                local_games = {row[7]: dict(zip(headers, row)) for row in sets[0]['rowSet']}  # GAME_ID as key
                official_games = await fetch_official_gamelogs(session, player_id, season, season_type)
                discrepancies = compare_gamelogs(local_games, official_games)
                for d in discrepancies:
                    d['PlayerID'] = player_id
                    d['Season'] = season
                    d['SeasonType'] = season_type
                results.extend(discrepancies)
                await asyncio.sleep(REQUEST_DELAY)
    # Write CSV report
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        fieldnames = ['PlayerID', 'Season', 'SeasonType', 'GAME_ID', 'Type', 'Field', 'Local', 'Official', 'Details']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"Full stats verification complete. Report written to {OUTPUT_FILE}")

if __name__ == "__main__":
    # Only run if executed directly
    asyncio.run(main()) 