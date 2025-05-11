"""
Script to collect data for multiple NBA players.
Designed to run in the background and handle interruptions gracefully.
"""
import asyncio
import json
import logging
import os
import signal
import sys
from datetime import datetime
from typing import Dict, Optional
from app.services.nba_collector import NBACollector, generate_seasons

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/collection/nba_bulk_collector.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('nba_bulk_collector')

# Global flag for graceful shutdown
shutdown_flag = False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_flag
    logger.info(f"Received signal {signum}. Starting graceful shutdown...")
    shutdown_flag = True

def load_player_ids() -> Dict[str, str]:
    """Load player IDs from the JSON file."""
    try:
        with open('data/players/nba_player_ids.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading player IDs: {str(e)}")
        sys.exit(1)

class CollectionProgress:
    """Track and manage collection progress."""
    def __init__(self, filename: str = "collection_progress.json"):
        self.filename = filename
        self.progress = self._load_progress()
        
    def _load_progress(self) -> Dict:
        """Load existing progress."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading progress file: {str(e)}")
                return {}
        return {}
    
    def save_progress(self):
        """Save current progress."""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.progress, f)
        except Exception as e:
            logger.error(f"Error saving progress: {str(e)}")
    
    def update_progress(self, player_id: str, season: str):
        """Update progress for a player and season."""
        if player_id not in self.progress:
            self.progress[player_id] = []
        if season not in self.progress[player_id]:
            self.progress[player_id].append(season)
            self.save_progress()
    
    def get_remaining_seasons(self, player_id: str, all_seasons: list) -> list:
        """Get remaining seasons to collect for a player."""
        if player_id in self.progress:
            return [s for s in all_seasons if s not in self.progress[player_id]]
        return all_seasons

async def collect_player_data(collector: NBACollector, player_id: str, player_name: str, 
                            seasons: list, progress_tracker: CollectionProgress):
    """Collect data for a single player with progress tracking."""
    remaining_seasons = progress_tracker.get_remaining_seasons(player_id, seasons)
    
    if not remaining_seasons:
        logger.info(f"All seasons already collected for {player_name} (ID: {player_id})")
        return
    
    logger.info(f"Starting collection for {player_name} (ID: {player_id}). {len(remaining_seasons)} seasons remaining")
    
    for season in remaining_seasons:
        if shutdown_flag:
            logger.info("Shutdown requested. Stopping collection...")
            break
            
        try:
            # Collect regular season data
            regular_season_data = await collector.fetch_player_stats(player_id, season, "Regular Season")
            if regular_season_data:
                logger.info(f"Successfully collected regular season data for {player_name} - {season}")
            await asyncio.sleep(collector.rate_limit_sleep)
            
            # Collect playoff data
            playoff_data = await collector.fetch_player_stats(player_id, season, "Playoffs")
            if playoff_data:
                logger.info(f"Successfully collected playoff data for {player_name} - {season}")
            await asyncio.sleep(collector.rate_limit_sleep)
            
            # Update progress only if both collections were successful
            if regular_season_data and playoff_data:
                progress_tracker.update_progress(player_id, season)
                
        except Exception as e:
            logger.error(f"Error collecting data for {player_name} (ID: {player_id}) season {season}: {str(e)}")
            continue

async def main():
    """Main function to run the collector."""
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Initialize collector and progress tracker
    collector = NBACollector()
    progress_tracker = CollectionProgress()
    
    # Load player IDs
    player_ids = load_player_ids()
    logger.info(f"Loaded {len(player_ids)} player IDs")
    
    # Generate seasons list (starting from 1996-97 when detailed stats became available)
    seasons = generate_seasons(start_year=1996)
    logger.info(f"Will collect data for seasons: {seasons[0]} to {seasons[-1]}")
    
    # Process each player
    for player_name, player_id in player_ids.items():
        if shutdown_flag:
            break
            
        await collect_player_data(collector, player_id, player_name, seasons, progress_tracker)
    
    logger.info("Collection process completed or interrupted. Shutting down...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1) 