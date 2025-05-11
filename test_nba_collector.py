from data_collector import NBADataCollector
import json
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_nba_collector():
    """Test the NBA data collector functionality."""
    collector = NBADataCollector()
    
    # Test players (using NBA.com player IDs)
    test_players = [
        "2544",  # LeBron James
        "201939",  # Stephen Curry
        "201142"  # Kevin Durant
    ]
    
    # Test collecting data for each player
    for player_id in test_players:
        print(f"\nCollecting data for player {player_id}...")
        player_data = collector.collect_player_data(player_id)
        
        if player_data and player_data['stats']:
            print(f"\nStats collected for player {player_id}:")
            
            for season_type, stats in player_data['stats'].items():
                print(f"\n{season_type} Stats:")
                if stats and len(stats) > 0:
                    print(f"Total games: {len(stats)}")
                    
                    # Print most recent game
                    recent_game = stats[0]
                    print("\nMost Recent Game:")
                    for stat, value in recent_game.items():
                        print(f"{stat}: {value}")
                else:
                    print("No stats available")
        else:
            print(f"Failed to collect data for player {player_id}")
            
if __name__ == "__main__":
    test_nba_collector() 