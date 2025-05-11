import os
import json
import time
import requests
from tqdm import tqdm
from datetime import datetime

# Config
TEAM_DATA_DIR = 'data/nfl/team_stats'
PLAYER_DATA_DIR = 'data/nfl/player_stats'
GAME_DATA_DIR = 'data/nfl/games'
current_year = datetime.now().year
SEASONS = [str(year) for year in range(current_year - 7, current_year + 2)]
NFL_TEAMS_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams'
NFL_TEAM_STATS_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/statistics'
NFL_TEAM_ROSTER_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/roster'
NFL_TEAM_SCHEDULE_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/schedule'
NFL_PLAYER_STATS_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/players/{player_id}/gamelog'
NFL_GAMES_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
NFL_GAME_BOX_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

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

def fetch_player_gamelog(player_id, season):
    url = NFL_PLAYER_STATS_URL.format(player_id=player_id)
    params = {'season': season}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if resp.status_code != 200:
        return None
    return resp.json()

def fetch_games_for_season(season):
    # ESPN API returns games by week, so we loop through weeks
    games = []
    for week in range(1, 23):  # NFL regular season + playoffs
        params = {'season': season, 'week': week}
        resp = requests.get(NFL_GAMES_URL, headers=HEADERS, params=params, timeout=10)
        if resp.status_code != 200:
            continue
        data = resp.json()
        events = data.get('events', [])
        for event in events:
            games.append(event)
        time.sleep(0.3)
    return games

def fetch_game_box(game_id):
    params = {'event': game_id}
    resp = requests.get(NFL_GAME_BOX_URL, headers=HEADERS, params=params, timeout=10)
    if resp.status_code != 200:
        return None
    return resp.json()

def main():
    teams = fetch_teams()
    print(f'Total teams: {len(teams)}')
    for season in SEASONS:
        print(f'\n=== {season} ===')
        # Team stats, rosters, schedules
        try:
            for team in tqdm(teams, desc=f'Teams in {season}'):
                team_dir = os.path.join(TEAM_DATA_DIR, team['abbreviation'])
                ensure_dir(team_dir)
                # Stats
                stats_path = os.path.join(team_dir, f'{season}_stats.json')
                if not os.path.exists(stats_path):
                    stats = fetch_team_stats(team['id'], season)
                    if stats:
                        with open(stats_path, 'w') as f:
                            json.dump(stats, f)
                    time.sleep(0.5)
                # Roster
                roster_path = os.path.join(team_dir, f'{season}_roster.json')
                if not os.path.exists(roster_path):
                    roster = fetch_team_roster(team['id'], season)
                    if roster:
                        with open(roster_path, 'w') as f:
                            json.dump(roster, f)
                    time.sleep(0.5)
                # Schedule
                schedule_path = os.path.join(team_dir, f'{season}_schedule.json')
                if not os.path.exists(schedule_path):
                    schedule = fetch_team_schedule(team['id'], season)
                    if schedule:
                        with open(schedule_path, 'w') as f:
                            json.dump(schedule, f)
                    time.sleep(0.5)
            print(f'Finished team stats/rosters/schedules for {season}')
        except Exception as e:
            print(f'Error in team stats/rosters/schedules for {season}: {e}')

        # Player stats and game logs
        try:
            for team in teams:
                team_dir = os.path.join(TEAM_DATA_DIR, team['abbreviation'])
                roster_path = os.path.join(team_dir, f'{season}_roster.json')
                if not os.path.exists(roster_path):
                    continue
                with open(roster_path) as f:
                    roster = json.load(f)
                athletes = roster.get('athletes', [])
                if not athletes:
                    print(f"Warning: No athletes found in roster for team {team['abbreviation']} in {season}.")
                for entry in athletes:
                    player = entry.get('athlete') or entry
                    player_id = player.get('id')
                    player_name = player.get('displayName', '').replace(' ', '-').lower() if player.get('displayName') else None
                    if not player_id or not player_name:
                        print(f"Skipping player with missing id or name in team {team['abbreviation']} for {season}.")
                        continue
                    print(f"Fetching gamelog for player {player_name} (ID: {player_id}) in {season}...")
                    gamelog = fetch_player_gamelog(player_id, season)
                    print(f"Finished fetching gamelog for player {player_name} (ID: {player_id}) in {season}.")
                    if gamelog:
                        with open(os.path.join(PLAYER_DATA_DIR, player_name, f'{season}.json'), 'w') as f:
                            json.dump(gamelog, f)
                    time.sleep(0.5)
            print(f'Finished player stats/gamelogs for {season}')
        except Exception as e:
            print(f'Error in player stats/gamelogs for {season}: {e}')

        # Game box scores
        try:
            games = fetch_games_for_season(season)
            print(f'Fetched {len(games)} games for {season}')
            season_game_dir = os.path.join(GAME_DATA_DIR, season)
            ensure_dir(season_game_dir)
            for game in tqdm(games, desc=f'Games in {season}'):
                game_id = game.get('id')
                if not game_id:
                    continue
                fpath = os.path.join(season_game_dir, f'{game_id}.json')
                if os.path.exists(fpath):
                    continue
                box = fetch_game_box(game_id)
                if box:
                    with open(fpath, 'w') as f:
                        json.dump(box, f)
                time.sleep(0.5)
            print(f'Finished game box scores for {season}')
        except Exception as e:
            print(f'Error in game box scores for {season}: {e}')
    print('Done!')

if __name__ == '__main__':
    main() 