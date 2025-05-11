import os
import json
from datetime import datetime
from sportsreference.nfl.teams import Teams

# Config
DATA_DIR = 'data/nfl_pfr'
current_year = datetime.now().year
SEASONS = [year for year in range(current_year - 7, current_year + 2)]

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    for season in SEASONS:
        print(f'=== {season} ===')
        season_dir = os.path.join(DATA_DIR, str(season))
        ensure_dir(season_dir)
        for team in Teams(year=season):
            team_abbr = team.abbreviation.lower()
            team_dir = os.path.join(season_dir, team_abbr)
            ensure_dir(team_dir)
            # Save team info
            team_info = {
                'name': team.name,
                'abbreviation': team.abbreviation,
                'conference': team.conference,
                'division': team.division,
                'record': team.record,
                'coach': team.coach,
                'games': team.games,
            }
            with open(os.path.join(team_dir, 'team_info.json'), 'w') as f:
                json.dump(team_info, f)
            # Save roster
            roster_data = []
            for player in team.roster.players:
                player_data = {
                    'name': player.name,
                    'player_id': player.player_id,
                    'position': player.position,
                    'height': player.height,
                    'weight': player.weight,
                    'birth_date': player.birth_date,
                    'college': player.college,
                    'games': player.games,
                    'stats': player.data,
                }
                roster_data.append(player_data)
                # Save individual player file
                player_dir = os.path.join(team_dir, 'players')
                ensure_dir(player_dir)
                with open(os.path.join(player_dir, f'{player.player_id}.json'), 'w') as pf:
                    json.dump(player_data, pf)
            with open(os.path.join(team_dir, 'roster.json'), 'w') as rf:
                json.dump(roster_data, rf)
        print(f'Finished {season}')
    print('Done!')

if __name__ == '__main__':
    main() 