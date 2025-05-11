import asyncio
import logging
from pathlib import Path
import sys
import os

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.nfl_service import NFLService
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/nfl_collector.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def collect_player_data(player_id: str, nfl_service: NFLService):
    """Collect both stats and game logs for a player."""
    try:
        logger.info(f"Collecting data for player {player_id}")
        
        # Collect current stats
        await nfl_service.collect_player_stats(player_id)
        logger.info(f"Collected stats for player {player_id}")
        
        # Collect game logs
        await nfl_service.collect_player_game_logs(player_id)
        logger.info(f"Collected game logs for player {player_id}")
        
    except Exception as e:
        logger.error(f"Error collecting data for player {player_id}: {e}")
        raise

async def collect_team_data(team_id: str, nfl_service: NFLService):
    """Collect team statistics."""
    try:
        logger.info(f"Collecting data for team {team_id}")
        await nfl_service.collect_team_stats(team_id)
        logger.info(f"Collected stats for team {team_id}")
    except Exception as e:
        logger.error(f"Error collecting data for team {team_id}: {e}")
        raise

async def main():
    """Main collection routine."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize service
        nfl_service = NFLService()
        
        # Example player IDs to collect (you would need to maintain this list)
        player_ids = [
            "patrick-mahomes",
            "travis-kelce",
            "aaron-rodgers"
        ]
        
        # Example team IDs
        team_ids = [
            "KC",  # Kansas City Chiefs
            "SF",  # San Francisco 49ers
            "GB"   # Green Bay Packers
        ]
        
        # Collect player data
        for player_id in player_ids:
            await collect_player_data(player_id, nfl_service)
            
        # Collect team data
        for team_id in team_ids:
            await collect_team_data(team_id, nfl_service)
            
    except Exception as e:
        logger.error(f"Error in main collection routine: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 