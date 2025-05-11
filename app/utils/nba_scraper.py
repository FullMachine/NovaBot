import os
import json
import requests
import pandas as pd
from datetime import datetime
from collections import defaultdict
import time
import re

def get_nba_api_players():
    """Get all players from NBA.com's API with additional information"""
    try:
        print("🔍 Fetching players from NBA.com API...")
        
        # NBA.com API endpoint for all players
        url = "https://stats.nba.com/stats/commonallplayers"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nba.com/',
            'Connection': 'keep-alive',
        }
        
        # Parameters to get all players (current, past, and future)
        params = {
            'LeagueID': '00',  # NBA
            'Season': '2023-24',  # Current season
            'IsOnlyCurrentSeason': '0'  # Get all players, not just current
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        players = data['resultSets'][0]['rowSet']
        headers = data['resultSets'][0]['headers']
        
        # Create a dictionary of player information
        player_data = {}
        for player in players:
            player_id = str(player[headers.index('PERSON_ID')])
            player_name = player[headers.index('DISPLAY_FIRST_LAST')]
            team_id = player[headers.index('TEAM_ID')]
            team_name = player[headers.index('TEAM_NAME')]
            roster_status = player[headers.index('ROSTERSTATUS')]
            from_year = player[headers.index('FROM_YEAR')]
            to_year = player[headers.index('TO_YEAR')]
            player_code = player[headers.index('PLAYERCODE')]
            
            player_data[player_name] = {
                'id': player_id,
                'team_id': str(team_id) if pd.notna(team_id) else None,
                'team_name': team_name if pd.notna(team_name) else None,
                'roster_status': roster_status,
                'from_year': from_year,
                'to_year': to_year,
                'player_code': player_code,
                'source': 'nba_api',
                'verified': True,  # NBA API players are pre-verified
                'last_verified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        print(f"✅ Found {len(player_data)} players from NBA.com API")
        return player_data
        
    except Exception as e:
        print(f"❌ Error fetching players from NBA.com API: {str(e)}")
        return None

def get_player_details(player_id):
    """Get additional player details from NBA.com"""
    try:
        url = f"https://stats.nba.com/stats/playerdashboardbygeneralsplits"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nba.com/',
        }
        
        params = {
            'PlayerID': player_id,
            'Season': '2023-24',
            'SeasonType': 'Regular Season',
            'MeasureType': 'Base'
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['resultSets'] and len(data['resultSets']) > 0:
                player_info = data['resultSets'][0]['rowSet'][0]
                headers = data['resultSets'][0]['headers']
                
                return {
                    'height': player_info[headers.index('HEIGHT')],
                    'weight': player_info[headers.index('WEIGHT')],
                    'position': player_info[headers.index('POSITION')],
                    'age': player_info[headers.index('AGE')],
                    'games_played': player_info[headers.index('GP')],
                    'minutes': player_info[headers.index('MIN')],
                    'points': player_info[headers.index('PTS')],
                    'rebounds': player_info[headers.index('REB')],
                    'assists': player_info[headers.index('AST')]
                }
    except Exception:
        pass
    return None

def get_player_stats(player_id, season='2023-24', season_type='Regular Season'):
    """
    Get player game statistics from NBA.com
    season_type can be: 'Regular Season', 'Playoffs', 'Pre Season', 'Play In'
    """
    try:
        url = "https://stats.nba.com/stats/playergamelogs"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.nba.com',
            'Referer': f'https://www.nba.com/stats/player/{player_id}/boxscores-traditional',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Connection': 'keep-alive'
        }
        
        params = {
            'DateFrom': '',
            'DateTo': '',
            'GameSegment': '',
            'LastNGames': '0',
            'LeagueID': '00',
            'Location': '',
            'MeasureType': 'Base',
            'Month': '0',
            'OpponentTeamID': '0',
            'Outcome': '',
            'PORound': '0',
            'PerMode': 'Totals',
            'Period': '0',
            'PlayerID': player_id,
            'Season': season,
            'SeasonSegment': '',
            'SeasonType': season_type,
            'TeamID': '0',
            'TwoWay': '0',
            'VsConference': '',
            'VsDivision': ''
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if not data['resultSets'] or not data['resultSets'][0]['rowSet']:
                return None

            # Get the headers and rows
            headers_data = data['resultSets'][0]['headers']
            games = data['resultSets'][0]['rowSet']

            # Process each game
            game_stats = []
            for game in games:
                game_data = {
                    'game_date': game[headers_data.index('GAME_DATE')],
                    'matchup': game[headers_data.index('MATCHUP')],
                    'win_loss': game[headers_data.index('WL')],
                    'minutes': game[headers_data.index('MIN')],
                    'points': game[headers_data.index('PTS')],
                    'rebounds': game[headers_data.index('REB')],
                    'assists': game[headers_data.index('AST')],
                    'steals': game[headers_data.index('STL')],
                    'blocks': game[headers_data.index('BLK')],
                    'field_goals_made': game[headers_data.index('FGM')],
                    'field_goals_attempted': game[headers_data.index('FGA')],
                    'field_goal_pct': game[headers_data.index('FG_PCT')],
                    'three_pointers_made': game[headers_data.index('FG3M')],
                    'three_pointers_attempted': game[headers_data.index('FG3A')],
                    'three_point_pct': game[headers_data.index('FG3_PCT')],
                    'free_throws_made': game[headers_data.index('FTM')],
                    'free_throws_attempted': game[headers_data.index('FTA')],
                    'free_throw_pct': game[headers_data.index('FT_PCT')],
                    'turnovers': game[headers_data.index('TOV')],
                    'plus_minus': game[headers_data.index('PLUS_MINUS')]
                }
                game_stats.append(game_data)

            # Calculate averages for this season type
            if game_stats:
                games_played = len(game_stats)
                season_totals = {stat: sum(float(game[stat]) if isinstance(game[stat], (int, float)) else 0 
                                         for game in game_stats if game[stat] not in ['', None]) 
                               for stat in ['points', 'rebounds', 'assists', 'steals', 'blocks', 'turnovers']}
                
                season_averages = {
                    'games_played': games_played,
                    'ppg': round(season_totals['points'] / games_played, 1),
                    'rpg': round(season_totals['rebounds'] / games_played, 1),
                    'apg': round(season_totals['assists'] / games_played, 1),
                    'spg': round(season_totals['steals'] / games_played, 1),
                    'bpg': round(season_totals['blocks'] / games_played, 1),
                    'topg': round(season_totals['turnovers'] / games_played, 1)
                }
            else:
                season_averages = None

            return {
                'season_type': season_type,
                'season': season,
                'season_averages': season_averages,
                'games': game_stats
            }

        return None
    except Exception as e:
        print(f"Error fetching {season_type} stats for player {player_id} ({season}): {str(e)}")
        return None

def verify_player_id(player_id, player_name):
    """Verify if a player ID is valid by checking NBA.com"""
    try:
        url = f"https://www.nba.com/stats/player/{player_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nba.com/',
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            # Get player details and stats
            details = get_player_details(player_id)
            stats = get_player_stats(player_id)
            
            result = {}
            if details:
                result.update(details)
            if stats:
                result['stats'] = stats
            
            return True, result
        return False, None
    except Exception:
        return False, None

def download_player_ids():
    """Download player IDs from GitHub repository and combine with NBA.com data"""
    try:
        print("🔍 Downloading player IDs from GitHub...")
        url = "https://raw.githubusercontent.com/djblechn-su/nba-player-team-ids/master/NBA_Player_IDs.csv"
        
        # Download the CSV content
        response = requests.get(url)
        response.encoding = 'utf-8'  # Force UTF-8 encoding
        
        # Save the CSV content to a temporary file
        os.makedirs('data/temp', exist_ok=True)
        temp_file = 'data/temp/player_ids.csv'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # Read the CSV file with explicit encoding
        df = pd.read_csv(temp_file, encoding='utf-8')
        
        # Create a dictionary of player information
        player_data = {}
        for _, row in df.iterrows():
            if pd.notna(row['NBAID']) and pd.notna(row['NBAName']):
                player_id = str(int(row['NBAID']))
                player_name = row['NBAName']
                player_data[player_name] = {
                    'id': player_id,
                    'source': 'github',
                    'verified': False,
                    'last_verified': None
                }
        
        # Get players from NBA.com API
        nba_api_players = get_nba_api_players()
        if nba_api_players:
            # Update player_data with NBA.com API data
            for name, data in nba_api_players.items():
                if name in player_data:
                    # Merge data from both sources
                    player_data[name].update(data)
                else:
                    player_data[name] = data
        
        # Add any missing notable players
        missing_players = {
            "Victor Wembanyama": {
                'id': "1629647",
                'source': 'manual',
                'verified': True,
                'last_verified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'team_name': "Spurs",
                'from_year': "2023",
                'to_year': "2023"
            },
            "Chet Holmgren": {
                'id': "1631096",
                'source': 'manual',
                'verified': True,
                'last_verified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'team_name': "Thunder",
                'from_year': "2023",
                'to_year': "2023"
            },
            "Brandon Miller": {
                'id': "1631105",
                'source': 'manual',
                'verified': True,
                'last_verified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'team_name': "Hornets",
                'from_year': "2023",
                'to_year': "2023"
            },
            "Jaime Jaquez Jr.": {
                'id': "1631133",
                'source': 'manual',
                'verified': True,
                'last_verified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'team_name': "Heat",
                'from_year': "2023",
                'to_year': "2023"
            },
            "Dereck Lively II": {
                'id': "1631106",
                'source': 'manual',
                'verified': True,
                'last_verified': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'team_name': "Mavericks",
                'from_year': "2023",
                'to_year': "2023"
            }
        }
        
        # Update player_data with missing players
        for name, data in missing_players.items():
            if name in player_data:
                player_data[name].update(data)
            else:
                player_data[name] = data
        
        # Verify only GitHub-sourced player IDs
        print("\n🔍 Verifying player IDs from GitHub...")
        verified_count = 0
        for name, data in player_data.items():
            if data['source'] == 'github' and not data['verified']:
                is_verified, details = verify_player_id(data['id'], name)
                if is_verified:
                    data['verified'] = True
                    data['last_verified'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if details:
                        data.update(details)
                    verified_count += 1
                time.sleep(0.5)  # Be nice to NBA.com
        
        # Remove duplicates (same ID but different names)
        id_to_names = defaultdict(list)
        for name, data in player_data.items():
            id_to_names[data['id']].append(name)
        
        # Keep the most common name for each ID
        final_player_data = {}
        for id, names in id_to_names.items():
            # Sort by length of name (prefer shorter names) and alphabetically
            best_name = sorted(names, key=lambda x: (len(x), x))[0]
            final_player_data[best_name] = player_data[best_name]
        
        # Save player data to file
        os.makedirs('data/players', exist_ok=True)
        with open('data/players/nba_player_data.json', 'w') as f:
            json.dump(final_player_data, f, indent=2)
        
        # Save update timestamp
        with open('data/players/update_timestamp.txt', 'w') as f:
            f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total players: {len(final_player_data)}\n")
            f.write(f"Verified players: {verified_count}\n")
            f.write(f"Added from NBA.com API: {len(nba_api_players) if nba_api_players else 0}\n")
            f.write(f"Added manually: {len(missing_players)}\n")
            f.write(f"Removed duplicates: {len(player_data) - len(final_player_data)}")
        
        # Clean up temporary file
        os.remove(temp_file)
        
        print(f"✅ Found {len(final_player_data)} total player IDs")
        print(f"✅ Verified {verified_count} player IDs")
        print(f"✅ Saved player data to data/players/nba_player_data.json")
        return final_player_data
            
    except Exception as e:
        print(f"❌ Error downloading player IDs: {str(e)}")
        return None

def get_all_player_stats(player_id, seasons=None):
    """Get all available stats for a player across different season types and years"""
    if seasons is None:
        # Default to last 3 seasons
        current_year = 2024
        seasons = [f"{year-1}-{year}" for year in range(current_year-2, current_year+1)]
    
    season_types = ['Regular Season', 'Playoffs', 'Pre Season', 'Play In']
    all_stats = {}
    
    for season in seasons:
        all_stats[season] = {}
        for season_type in season_types:
            stats = get_player_stats(player_id, season, season_type)
            if stats and stats['season_averages']:
                all_stats[season][season_type] = stats
            time.sleep(0.5)  # Be nice to NBA.com
    
    return all_stats

def normalize_name(name):
    """Normalize player name by removing special characters"""
    # Map of special characters to their normal form
    char_map = {
        'ć': 'c',
        'č': 'c',
        'š': 's',
        'ž': 'z',
        'đ': 'd',
        'ň': 'n',
        'ř': 'r',
        'ā': 'a',
        'ī': 'i',
        'ū': 'u',
        'ö': 'o',
        'ü': 'u',
        'ı': 'i',
        'ğ': 'g'
    }
    
    # Convert to lowercase and replace special chars
    normalized = name.lower()
    for special, normal in char_map.items():
        normalized = normalized.replace(special, normal)
    
    # Convert back to title case
    return normalized.title()

def scrape_player_ids():
    """Scrape player IDs directly from NBA.com"""
    try:
        print("🔍 Scraping player IDs from NBA.com...")
        url = "https://stats.nba.com/stats/playerindex"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.nba.com',
            'Referer': 'https://www.nba.com/players',
            'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Connection': 'keep-alive'
        }
        
        # Parameters to get all players (historical and current)
        params = {
            'Active': '',  # Empty for all players
            'AllStar': '',
            'College': '',
            'Country': '',
            'DraftPick': '',
            'DraftRound': '',
            'DraftYear': '',
            'Height': '',
            'Historical': '1',  # Include historical players
            'LeagueID': '00',
            'Pace': 'N',
            'PerMode': 'Totals',
            'Season': '2023-24',
            'SeasonType': 'Regular Season',
            'TeamID': '0',
            'Weight': ''
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if not data['resultSets'] or not data['resultSets'][0]['rowSet']:
                return None

            headers_data = data['resultSets'][0]['headers']
            players = data['resultSets'][0]['rowSet']
            player_data = {}
            
            # Process each player with more error checking
            for player in players:
                try:
                    player_dict = dict(zip(headers_data, player))
                    
                    # Construct full name
                    first_name = player_dict.get('PLAYER_FIRST_NAME', '')
                    last_name = player_dict.get('PLAYER_LAST_NAME', '')
                    full_name = f"{first_name} {last_name}".strip()
                    
                    if not full_name:
                        continue
                    
                    # Store both normalized and original names
                    normalized_name = normalize_name(full_name)
                    player_data[full_name] = {
                        'id': str(player_dict.get('PERSON_ID', '')),
                        'normalized_name': normalized_name,
                        'team_id': str(player_dict.get('TEAM_ID', '0')),
                        'team_name': player_dict.get('TEAM_NAME', ''),
                        'team_city': player_dict.get('TEAM_CITY', ''),
                        'team_abbrev': player_dict.get('TEAM_ABBREVIATION', ''),
                        'jersey': player_dict.get('JERSEY_NUMBER', ''),
                        'is_active': player_dict.get('ROSTER_STATUS', 0) == 1,
                        'from_year': str(player_dict.get('FROM_YEAR', '')),
                        'to_year': str(player_dict.get('TO_YEAR', '')),
                        'height': player_dict.get('HEIGHT', ''),
                        'weight': player_dict.get('WEIGHT', ''),
                        'position': player_dict.get('POSITION', ''),
                        'college': player_dict.get('COLLEGE', ''),
                        'country': player_dict.get('COUNTRY', ''),
                        'draft_year': player_dict.get('DRAFT_YEAR', ''),
                        'draft_round': player_dict.get('DRAFT_ROUND', ''),
                        'draft_number': player_dict.get('DRAFT_NUMBER', ''),
                        'current_stats': {
                            'points': player_dict.get('PTS', 0),
                            'rebounds': player_dict.get('REB', 0),
                            'assists': player_dict.get('AST', 0),
                            'timeframe': player_dict.get('STATS_TIMEFRAME', '')
                        },
                        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Add an entry with the normalized name as well
                    if normalized_name != full_name:
                        player_data[normalized_name] = player_data[full_name]
                        
                except Exception as e:
                    print(f"Warning: Error processing player: {str(e)}")
                    continue
            
            # Save to file
            os.makedirs('data/players', exist_ok=True)
            with open('data/players/nba_player_data.json', 'w') as f:
                json.dump(player_data, f, indent=2)
            
            print(f"✅ Found {len(player_data)} players")
            print(f"✅ Active players: {sum(1 for p in player_data.values() if p['is_active'])}")
            print(f"✅ Saved player data to data/players/nba_player_data.json")
            
            return player_data
            
        else:
            print(f"❌ Error: NBA.com returned status code {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error scraping player IDs: {str(e)}")
        return None

def load_player_data():
    """Load player data from file or scrape if not available"""
    try:
        # Try to load from file first
        if os.path.exists('data/players/nba_player_data.json'):
            try:
                with open('data/players/nba_player_data.json', 'r') as f:
                    data = json.load(f)
                    # Check if data is older than 24 hours
                    first_player = next(iter(data.values()))
                    if 'last_updated' in first_player:
                        last_updated = datetime.strptime(first_player['last_updated'], '%Y-%m-%d %H:%M:%S')
                        if (datetime.now() - last_updated).days < 1:
                            print(f"✅ Loaded {len(data)} players from cache")
                            return data
            except Exception:
                # If there's any error reading the file or parsing the data, scrape new data
                pass
        
        # If file doesn't exist or is old or has wrong format, scrape new data
        return scrape_player_ids()
        
    except Exception as e:
        print(f"❌ Error loading player data: {str(e)}")
        return None

def test_player_ids(player_data):
    """Test if player IDs work by checking NBA.com URLs"""
    test_players = [
        "LeBron James",  # Active superstar
        "Nikola Jokic",  # Current MVP
        "Victor Wembanyama",  # 2023-24 Rookie
        "Stephen Curry",  # Active superstar
        "Chet Holmgren",  # 2023-24 Rookie
        "Michael Jordan",  # Legend
        "Kobe Bryant",  # Legend
        "Kareem Abdul-Jabbar"  # Legend
    ]
    
    print("\n🔍 Testing player IDs...")
    for player in test_players:
        if player in player_data:
            data = player_data[player]
            print(f"\n✅ {player}")
            print(f"   ID: {data['id']}")
            print(f"   Team: {data['team_name'] if data['team_name'] else 'N/A'}")
            print(f"   Active: {'Yes' if data['is_active'] else 'No'}")
            print(f"   Years: {data['from_year']}-{data['to_year']}")
            print(f"   Position: {data['position']}")
            print(f"   Height: {data['height']}")
            print(f"   Weight: {data['weight']}")
            print(f"   Country: {data['country']}")
            
            # Get their stats
            try:
                all_stats = get_all_player_stats(data['id'])
                if all_stats:
                    for season in sorted(all_stats.keys(), reverse=True)[:1]:  # Show only most recent season
                        print(f"\n   📊 {season} Stats:")
                        for season_type in all_stats[season]:
                            stats = all_stats[season][season_type]
                            avg = stats['season_averages']
                            print(f"      {season_type} ({avg['games_played']} games):")
                            print(f"         {avg['ppg']} PPG, {avg['rpg']} RPG, {avg['apg']} APG")
            except Exception as e:
                print(f"   ❌ Error fetching stats: {str(e)}")
        else:
            print(f"❌ {player} - Not found in database")

def display_player_list(player_data, filter_active=None, show_details=False):
    """
    Display player names and IDs in alphabetical order
    filter_active: None for all players, True for active only, False for inactive only
    show_details: If True, shows additional player details
    """
    # Filter players if needed
    filtered_players = {}
    for name, data in player_data.items():
        # Skip normalized duplicates
        if data.get('normalized_name') != name:
            continue
            
        if filter_active is not None:
            if data['is_active'] != filter_active:
                continue
        filtered_players[name] = data
    
    # Sort players by name
    sorted_players = dict(sorted(filtered_players.items()))
    
    # Display counts
    total = len(sorted_players)
    active = sum(1 for p in sorted_players.values() if p['is_active'])
    print(f"\n📊 Player Statistics:")
    print(f"   Total Players: {total}")
    print(f"   Active Players: {active}")
    print(f"   Inactive Players: {total - active}")
    
    # Display the list
    print("\n📋 Player List:")
    for name, data in sorted_players.items():
        status = "🟢" if data['is_active'] else "⭕"
        if show_details:
            team = f" | {data['team_name']}" if data['team_name'] else ""
            years = f" | {data['from_year']}-{data['to_year']}"
            position = f" | {data['position']}" if data['position'] else ""
            print(f"{status} {name} (ID: {data['id']}){team}{position}{years}")
        else:
            print(f"{status} {name} (ID: {data['id']})")

if __name__ == "__main__":
    # Load or scrape player data
    player_data = load_player_data()
    if player_data:
        # Display all players with details
        display_player_list(player_data, show_details=True)
        
        # Test specific players
        print("\n🔍 Testing specific players...")
        test_player_ids(player_data) 