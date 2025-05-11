import asyncio
import logging
from pathlib import Path
import sys
import os
from typing import List, Dict
from datetime import datetime

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.nfl_service import NFLService
from app.services.soccer_service import SoccerService
from app.services.tennis_service import TennisService
from app.services.esports_service import EsportsService
from app.services.combat_sports_service import CombatSportsService
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sports_collector.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SportsDataCollector:
    def __init__(self):
        # Initialize services
        self.nfl_service = NFLService()
        
        # Soccer services for different leagues
        self.soccer_services = {
            league_id: SoccerService(league_id)
            for league_id in ['epl', 'laliga', 'seriea', 'bundesliga', 'ligue1', 'mls', 'ucl']
        }
        
        # Tennis services
        self.tennis_services = {
            tour: TennisService(tour)
            for tour in ['atp', 'wta']
        }
        
        # Esports services
        self.esports_services = {
            game: EsportsService(game)
            for game in ['lol', 'dota2', 'csgo', 'valorant', 'overwatch']
        }
        
        # Combat sports services
        self.combat_services = {
            sport: CombatSportsService(sport)
            for sport in ['ufc', 'boxing']
        }

    async def collect_nfl_data(self):
        """Collect NFL data."""
        try:
            logger.info("Starting NFL data collection")
            
            # Example player IDs (expand this list)
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
            
            for player_id in player_ids:
                await self.nfl_service.collect_player_stats(player_id)
                await self.nfl_service.collect_player_game_logs(player_id)
                
            for team_id in team_ids:
                await self.nfl_service.collect_team_stats(team_id)
                
        except Exception as e:
            logger.error(f"Error collecting NFL data: {e}")

    async def collect_soccer_data(self):
        """Collect soccer data for all leagues."""
        try:
            logger.info("Starting soccer data collection")
            
            for league_id, service in self.soccer_services.items():
                logger.info(f"Collecting data for {league_id}")
                
                # Example team IDs (customize per league)
                team_ids = ["real-madrid", "barcelona"] if league_id == "laliga" else ["man-city", "arsenal"]
                
                # Collect league table
                await service.get_league_table()
                
                # Collect team stats
                for team_id in team_ids:
                    await service.collect_team_stats(team_id)
                    
                # Collect fixtures
                await service.get_fixtures()
                
        except Exception as e:
            logger.error(f"Error collecting soccer data: {e}")

    async def collect_tennis_data(self):
        """Collect tennis data for both tours."""
        try:
            logger.info("Starting tennis data collection")
            
            for tour, service in self.tennis_services.items():
                logger.info(f"Collecting data for {tour}")
                
                # Example player IDs (customize per tour)
                player_ids = ["djokovic", "alcaraz"] if tour == "atp" else ["swiatek", "gauff"]
                
                # Collect rankings
                await service.get_rankings()
                
                # Collect player stats
                for player_id in player_ids:
                    await service.collect_player_stats(player_id)
                    
                # Collect tournament data
                # Add tournament IDs as needed
                
        except Exception as e:
            logger.error(f"Error collecting tennis data: {e}")

    async def collect_esports_data(self):
        """Collect esports data for all games."""
        try:
            logger.info("Starting esports data collection")
            
            for game, service in self.esports_services.items():
                logger.info(f"Collecting data for {game}")
                
                # Example team IDs (customize per game)
                team_ids = ["t1", "geng"] if game == "lol" else ["navi", "vitality"]
                
                # Collect rankings
                await service.get_rankings()
                
                # Collect team stats
                for team_id in team_ids:
                    await service.collect_team_stats(team_id)
                    
                # Collect tournament data
                await service.get_tournament_data("current_major")
                
        except Exception as e:
            logger.error(f"Error collecting esports data: {e}")

    async def collect_combat_sports_data(self):
        """Collect combat sports data."""
        try:
            logger.info("Starting combat sports data collection")
            
            for sport, service in self.combat_services.items():
                logger.info(f"Collecting data for {sport}")
                
                # Example fighter IDs (customize per sport)
                fighter_ids = ["jon-jones", "islam-makhachev"] if sport == "ufc" else ["canelo", "fury"]
                
                # Collect rankings for each weight class
                for weight_class in service.weight_classes:
                    await service.get_rankings(weight_class)
                
                # Collect fighter stats
                for fighter_id in fighter_ids:
                    await service.collect_fighter_stats(fighter_id)
                    await service.get_fight_history(fighter_id)
                    
                # Collect upcoming events
                await service.get_upcoming_events()
                
        except Exception as e:
            logger.error(f"Error collecting combat sports data: {e}")

    async def collect_all_data(self):
        """Collect data for all sports."""
        try:
            collection_tasks = [
                self.collect_nfl_data(),
                self.collect_soccer_data(),
                self.collect_tennis_data(),
                self.collect_esports_data(),
                self.collect_combat_sports_data()
            ]
            
            await asyncio.gather(*collection_tasks)
            
        except Exception as e:
            logger.error(f"Error in main collection routine: {e}")
            sys.exit(1)

async def main():
    """Main execution function."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize collector
        collector = SportsDataCollector()
        
        # Collect all data
        await collector.collect_all_data()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 