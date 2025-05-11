import json
import os
import requests
from typing import Dict, List
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('verification.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def verify_player_stats(player_file: str) -> Dict:
    """Verify a player's stats against NBA.com"""
    with open(player_file, 'r') as f:
        data = json.load(f)
    
    player_id = data['player_id']
    player_name = data['stats']['Regular Season'][0]['PLAYER_NAME']
    
    # Get official stats from NBA.com
    url = f"https://stats.nba.com/stats/playergamelog?PlayerID={player_id}&Season=2023-24&SeasonType=Regular%20Season"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://www.nba.com',
        'Referer': 'https://www.nba.com/',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true'
    }
    
    try:
        response = requests.get(url, headers=headers)
        official_data = response.json()
        
        # Compare stats
        our_games = len(data['stats']['Regular Season'])
        official_games = len(official_data['resultSets'][0]['rowSet'])
        
        return {
            'player_name': player_name,
            'player_id': player_id,
            'our_games': our_games,
            'official_games': official_games,
            'matches': our_games == official_games,
            'last_verified': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error verifying {player_name}: {str(e)}")
        return {
            'player_name': player_name,
            'player_id': player_id,
            'error': str(e),
            'last_verified': datetime.now().isoformat()
        }

def main():
    player_files = [f for f in os.listdir('data/nba') if f.startswith('player_') and f.endswith('.json')]
    verification_results = []
    
    for player_file in player_files:
        logger.info(f"Verifying {player_file}...")
        result = verify_player_stats(os.path.join('data/nba', player_file))
        verification_results.append(result)
        
        if 'error' in result:
            logger.error(f"Failed to verify {result['player_name']}: {result['error']}")
        else:
            logger.info(f"Verified {result['player_name']}: {result['our_games']} games (matches: {result['matches']})")
    
    # Save verification results
    with open('verification_results.json', 'w') as f:
        json.dump(verification_results, f, indent=2)
    
    # Print summary
    total_players = len(verification_results)
    successful_verifications = sum(1 for r in verification_results if 'error' not in r and r['matches'])
    logger.info(f"\nVerification Summary:")
    logger.info(f"Total players: {total_players}")
    logger.info(f"Successfully verified: {successful_verifications}")
    logger.info(f"Failed verifications: {total_players - successful_verifications}")

if __name__ == "__main__":
    main() 