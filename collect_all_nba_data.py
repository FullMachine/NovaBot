from data_collector import NBADataCollector
import logging
from datetime import datetime
import time
from typing import List
import json
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('collection_progress.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def load_progress() -> set:
    """Load the set of already processed player IDs."""
    try:
        if os.path.exists('processed_players.json'):
            with open('processed_players.json', 'r') as f:
                return set(json.load(f))
    except Exception as e:
        logger.error(f"Error loading progress: {e}")
    return set()

def save_progress(processed_ids: set):
    """Save the set of processed player IDs."""
    try:
        with open('processed_players.json', 'w') as f:
            json.dump(list(processed_ids), f)
    except Exception as e:
        logger.error(f"Error saving progress: {e}")

def generate_seasons(start_year: int = 1946) -> List[str]:
    """Generate NBA season strings from start_year to current season."""
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # If we're in the first half of the year, use previous season
    if current_month < 7:
        current_year -= 1
    
    seasons = []
    for year in range(start_year, current_year + 1):
        seasons.append(f"{year}-{str(year+1)[-2:]}")
    return seasons

def main():
    collector = NBADataCollector()
    processed_ids = load_progress()
    
    # Get all players
    players = collector.get_all_players()
    if not players:
        logger.error("Failed to get player list")
        return
    
    total_players = len(players)
    logger.info(f"Found {total_players} players")
    
    # Generate seasons from 1946 to current
    seasons = generate_seasons()
    logger.info(f"Collecting data for {len(seasons)} seasons")
    
    # Create data directory if it doesn't exist
    Path('data/nba').mkdir(parents=True, exist_ok=True)
    
    # Track successful and failed players
    successful = 0
    failed = 0
    
    try:
        # Collect data for each player
        for i, player in enumerate(players):
            player_id = str(player['PERSON_ID'])
            player_name = player['DISPLAY_FIRST_LAST']
            
            # Skip if already processed
            if player_id in processed_ids:
                logger.info(f"Skipping already processed player: {player_name} (ID: {player_id})")
                continue
            
            logger.info(f"\nProcessing player {i+1}/{total_players}: {player_name} (ID: {player_id})")
            
            try:
                # Collect data for all seasons
                player_data = collector.collect_player_data(player_id, seasons)
                
                if player_data:
                    logger.info(f"Successfully collected data for {player_name}")
                    successful += 1
                    processed_ids.add(player_id)
                    save_progress(processed_ids)
                else:
                    logger.error(f"Failed to collect data for {player_name}")
                    failed += 1
                
            except Exception as e:
                logger.error(f"Error processing {player_name}: {str(e)}")
                failed += 1
                continue
            
            # Log progress
            progress = (i + 1) / total_players * 100
            logger.info(f"Progress: {progress:.2f}% ({successful} successful, {failed} failed)")
            
    except KeyboardInterrupt:
        logger.info("\nCollection interrupted by user")
    finally:
        # Save final progress
        save_progress(processed_ids)
        logger.info(f"\nCollection finished. Successfully processed {successful} players, failed {failed} players")
        logger.info(f"Progress saved to processed_players.json")

if __name__ == "__main__":
    main() 