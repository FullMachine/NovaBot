import json
from operator import itemgetter
import requests
import time
import csv
from datetime import datetime

def get_player_details(player_id):
    """Get detailed player information from NBA API"""
    try:
        url = f"https://stats.nba.com/stats/commonplayerinfo?PlayerID={player_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nba.com/',
            'Connection': 'keep-alive',
        }
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'resultSets' in data and len(data['resultSets']) > 0:
                headers = data['resultSets'][0]['headers']
                rows = data['resultSets'][0]['rowSet']
                if rows:
                    player_info = dict(zip(headers, rows[0]))
                    return {
                        'team': player_info.get('TEAM_NAME', 'N/A'),
                        'position': player_info.get('POSITION', 'N/A'),
                        'height': player_info.get('HEIGHT', 'N/A'),
                        'weight': player_info.get('WEIGHT', 'N/A'),
                        'birth_date': player_info.get('BIRTH_DATE', 'N/A'),
                        'active': player_info.get('ROSTERSTATUS', 'N/A')
                    }
        return None
    except:
        return None

def verify_player_id(player_id):
    """Verify if a player ID exists in the NBA API"""
    try:
        url = f"https://stats.nba.com/stats/commonplayerinfo?PlayerID={player_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nba.com/',
            'Connection': 'keep-alive',
        }
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code == 200
    except:
        return False

def export_players(players, filename=None):
    """Export player data to CSV file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nba_players_{timestamp}.csv"
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Player Name', 'Player ID', 'Team', 'Position', 'Height', 'Weight', 'Birth Date', 'Active'])
        for player in players:
            writer.writerow([
                player['name'],
                player['id'],
                player.get('team', 'N/A'),
                player.get('position', 'N/A'),
                player.get('height', 'N/A'),
                player.get('weight', 'N/A'),
                player.get('birth_date', 'N/A'),
                player.get('active', 'N/A')
            ])
    return filename

def view_player_ids(search_term=None, verify=False, export=False, details=False):
    try:
        # Load the player IDs
        with open('data/players/nba_player_ids.json', 'r') as f:
            player_data = json.load(f)
        
        # Convert to list of tuples and sort alphabetically
        players = [(name, pid) for name, pid in player_data.items()]
        players.sort(key=itemgetter(0))  # Sort by player name
        
        # Filter by search term if provided
        if search_term:
            search_term = search_term.lower()
            players = [(name, pid) for name, pid in players if search_term in name.lower()]
        
        # Process players and gather details
        processed_players = []
        verified_count = 0
        
        for name, pid in players:
            player_info = {'name': name, 'id': pid}
            
            if verify or details:
                if verify_player_id(pid):
                    verified_count += 1
                    player_info['verified'] = True
                    if details:
                        details = get_player_details(pid)
                        if details:
                            player_info.update(details)
                else:
                    player_info['verified'] = False
            
            processed_players.append(player_info)
        
        # Display the results
        print("\nNBA Player IDs (Alphabetical Order):")
        print("-" * 100)
        header = f"{'Player Name':<30} {'Player ID':<10}"
        if verify:
            header += " {'Verified':<10}"
        if details:
            header += f" {'Team':<20} {'Position':<10} {'Active':<8}"
        print(header)
        print("-" * 100)
        
        for player in processed_players:
            line = f"{player['name']:<30} {player['id']:<10}"
            if verify:
                line += f" {'✓' if player.get('verified') else '':<10}"
            if details:
                line += f" {player.get('team', 'N/A'):<20} {player.get('position', 'N/A'):<10} {player.get('active', 'N/A'):<8}"
            print(line)
        
        print(f"\nTotal Players: {len(processed_players)}")
        if verify:
            print(f"Verified Players: {verified_count}")
        
        # Export if requested
        if export:
            filename = export_players(processed_players)
            print(f"\nData exported to: {filename}")
        
    except FileNotFoundError:
        print("Error: Could not find nba_player_ids.json file")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the file")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='View NBA Player IDs')
    parser.add_argument('--search', type=str, help='Search for a specific player')
    parser.add_argument('--verify', action='store_true', help='Verify player IDs against NBA API')
    parser.add_argument('--export', action='store_true', help='Export data to CSV file')
    parser.add_argument('--details', action='store_true', help='Show detailed player information')
    args = parser.parse_args()
    
    view_player_ids(args.search, args.verify, args.export, args.details) 