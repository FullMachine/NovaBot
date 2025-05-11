import os
import json
import time
import requests
from tqdm import tqdm

DATA_DIR = 'data/nfl/team_stats'
SEASONS = [str(year) for year in range(2000, 2024)]
NFL_TEAMS_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams'
NFL_TEAM_STATS_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics'
NFL_TEAM_ROSTER_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/roster'
NFL_TEAM_SCHEDULE_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

def fetch_teams():
    resp = requests.get(NFL_TEAMS_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    teams = []
    for item in data.get('sports', [])[0].get('leagues', [])[0].get('teams', []):
        team = item.get('team')
        if team:
            teams.append({
                'id': team.get('id'),
                'abbreviation': team.get('abbreviation').lower(),
                'displayName': team.get('displayName'),
            })
    return teams

def fetch_team_stats(team_id, season):
    url = NFL_TEAM_STATS_URL.format(team_id=team_id)
    params = {'season': season}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if resp.status_code != 200:
        return None
    return resp.json()

def fetch_team_roster(team_id, season):
    url = NFL_TEAM_ROSTER_URL.format(team_id=team_id)
    params = {'season': season}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if resp.status_code != 200:
        return None
    return resp.json()

def fetch_team_schedule(team_id, season):
    url = NFL_TEAM_SCHEDULE_URL.format(team_id=team_id)
    params = {'season': season}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if resp.status_code != 200:
        return None
    return resp.json()

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    teams = fetch_teams()
    print(f'Total teams: {len(teams)}')
    for season in SEASONS:
        print(f'\n=== {season} ===')
        for team in tqdm(teams, desc=f'Teams in {season}'):
            team_dir = os.path.join(DATA_DIR, team['abbreviation'])
            ensure_dir(team_dir)
            # Stats
            stats_path = os.path.join(team_dir, f'{season}_stats.json')
            if not os.path.exists(stats_path):
                stats = fetch_team_stats(team['id'], season)
                if stats:
                    with open(stats_path, 'w') as f:
                        json.dump(stats, f)
                    tqdm.write(f'Saved stats for {team["displayName"]} ({season})')
                else:
                    tqdm.write(f'No stats for {team["displayName"]} ({season})')
                time.sleep(0.5)
            # Roster
            roster_path = os.path.join(team_dir, f'{season}_roster.json')
            if not os.path.exists(roster_path):
                roster = fetch_team_roster(team['id'], season)
                if roster:
                    with open(roster_path, 'w') as f:
                        json.dump(roster, f)
                    tqdm.write(f'Saved roster for {team["displayName"]} ({season})')
                else:
                    tqdm.write(f'No roster for {team["displayName"]} ({season})')
                time.sleep(0.5)
            # Schedule
            schedule_path = os.path.join(team_dir, f'{season}_schedule.json')
            if not os.path.exists(schedule_path):
                schedule = fetch_team_schedule(team['id'], season)
                if schedule:
                    with open(schedule_path, 'w') as f:
                        json.dump(schedule, f)
                    tqdm.write(f'Saved schedule for {team["displayName"]} ({season})')
                else:
                    tqdm.write(f'No schedule for {team["displayName"]} ({season})')
                time.sleep(0.5)
    print('Done!')

if __name__ == '__main__':
    main() 