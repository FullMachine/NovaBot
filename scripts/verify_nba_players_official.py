import json
import csv
import aiohttp
import asyncio
import time
from typing import Dict, List

NBA_PLAYER_INFO_URL = "https://stats.nba.com/stats/commonplayerinfo?PlayerID={player_id}"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.nba.com',
    'Accept': 'application/json'
}

INPUT_FILE = "data/players/nba_player_ids_verified.json"
OUTPUT_FILE = "verify_nba_players_full_report.csv"
REQUEST_DELAY = 0.5  # seconds

async def fetch_player_info(session, player_id: str) -> Dict:
    url = NBA_PLAYER_INFO_URL.format(player_id=player_id)
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            if data['resultSets'][0]['rowSet']:
                headers = data['resultSets'][0]['headers']
                values = data['resultSets'][0]['rowSet'][0]
                return dict(zip(headers, values))
        return {}

def compare_player_details(local_name: str, local_id: str, nba_data: Dict) -> Dict:
    discrepancies = {}
    # Compare name
    nba_name = nba_data.get('DISPLAY_FIRST_LAST', '').strip()
    if nba_name and nba_name.lower() != local_name.lower():
        discrepancies['name'] = {'local': local_name, 'nba': nba_name}
    # Compare ID
    nba_id = str(nba_data.get('PERSON_ID', '')).strip()
    if nba_id and nba_id != local_id:
        discrepancies['id'] = {'local': local_id, 'nba': nba_id}
    # Compare team
    local_team = None  # Not available in local file, placeholder for future
    nba_team = nba_data.get('TEAM_NAME', '').strip()
    # Compare position
    local_pos = None  # Not available in local file, placeholder for future
    nba_pos = nba_data.get('POSITION', '').strip()
    # Add to discrepancies if needed (future expansion)
    return {
        'Player Name': local_name,
        'Local ID': local_id,
        'NBA.com Name': nba_name,
        'NBA.com ID': nba_id,
        'NBA.com Team': nba_team,
        'NBA.com Position': nba_pos,
        'Discrepancies': discrepancies
    }

async def main():
    # Load all players
    with open(INPUT_FILE, 'r') as f:
        player_dict = json.load(f)
    all_players = list(player_dict.items())

    results = []
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for idx, (name, player_id) in enumerate(all_players, 1):
            nba_data = await fetch_player_info(session, player_id)
            if nba_data:
                result = compare_player_details(name, player_id, nba_data)
            else:
                result = {
                    'Player Name': name,
                    'Local ID': player_id,
                    'NBA.com Name': '',
                    'NBA.com ID': '',
                    'NBA.com Team': '',
                    'NBA.com Position': '',
                    'Discrepancies': {'error': 'No data from NBA.com'}
                }
            results.append(result)
            if idx % 25 == 0:
                print(f"Verified {idx} players...")
            await asyncio.sleep(REQUEST_DELAY)

    # Write CSV report
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        fieldnames = ['Player Name', 'Local ID', 'NBA.com Name', 'NBA.com ID', 'NBA.com Team', 'NBA.com Position', 'Discrepancies']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            row['Discrepancies'] = json.dumps(row['Discrepancies'])
            writer.writerow(row)
    print(f"Full verification complete. Report written to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main()) 