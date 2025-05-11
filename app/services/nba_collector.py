"""
NBA data collector service with robust error handling and retries.
"""
import logging
import os
import json
import aiohttp
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from aiohttp import ClientTimeout
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/collection/nba_collector.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('nba_collector')

def generate_seasons(start_year: int = 1946, end_year: Optional[int] = None) -> List[str]:
    """Generate a list of NBA seasons from start_year to current year."""
    if end_year is None:
        end_year = datetime.now().year
        # If we're past July, include next season
        if datetime.now().month > 7:
            end_year += 1
    
    seasons = []
    for year in range(start_year, end_year):
        season = f"{year}-{str(year + 1)[2:]}"
        seasons.append(season)
    return seasons

class NBACollector:
    """NBA data collector service with robust error handling."""
    
    def __init__(self):
        """Initialize the NBA collector."""
        self.base_url = "https://stats.nba.com/stats"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.nba.com',
            'Referer': 'https://www.nba.com/',
            'x-nba-stats-origin': 'stats',
            'x-nba-stats-token': 'true'
        }
        self.rate_limit = int(os.getenv("NBA_RATE_LIMIT", 60))
        self.rate_limit_sleep = 60 / self.rate_limit  # Sleep time between requests
        self.timeout = ClientTimeout(total=30)  # 30 second timeout
        
    def _get_storage_path(self, season: str, player_id: str, season_type: str) -> str:
        """Get the storage path for player stats."""
        base_dir = f"data/nba/player_stats/{season}"
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, f"{player_id}_{season_type.lower().replace(' ', '_')}.json")
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def fetch_player_stats(self, player_id: str, season: str, season_type: str = "Regular Season") -> Dict:
        """Fetch player statistics from NBA.com with retries."""
        endpoint = f"{self.base_url}/playergamelogs"
        params = {
            'PlayerID': player_id,
            'SeasonType': season_type,
            'Season': season,
            'DateFrom': '',
            'DateTo': '',
            'LastNGames': '82',
            'Location': '',
            'Month': '0',
            'OpponentTeamID': '0',
            'Outcome': '',
            'SeasonSegment': '',
            'VsConference': '',
            'VsDivision': ''
        }
        
        storage_path = self._get_storage_path(season, player_id, season_type)
        
        # Check if data already exists and is valid
        if os.path.exists(storage_path):
            try:
                with open(storage_path, 'r') as f:
                    existing_data = json.load(f)
                if existing_data and 'resultSets' in existing_data:
                    logger.info(f"Using cached data for player {player_id} season {season} ({season_type})")
                    return existing_data
            except json.JSONDecodeError:
                logger.warning(f"Invalid cached data found for {storage_path}, will refetch")
                os.remove(storage_path)
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(endpoint, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Validate response data
                        if not data or 'resultSets' not in data:
                            raise ValueError("Invalid response data format")
                        
                        # Save the data atomically using a temporary file
                        temp_path = f"{storage_path}.tmp"
                        try:
                            with open(temp_path, 'w') as f:
                                json.dump(data, f)
                            os.replace(temp_path, storage_path)
                        except Exception as e:
                            logger.error(f"Error saving data: {str(e)}")
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                            raise
                            
                        return data
                    else:
                        error_msg = f"Error fetching data: {response.status}"
                        logger.error(error_msg)
                        raise aiohttp.ClientError(error_msg)
                        
        except asyncio.TimeoutError:
            logger.error(f"Timeout while fetching data for player {player_id} season {season}")
            raise
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise
            
    async def collect_player_data(self, player_id: str, seasons: list):
        """Collect player data for multiple seasons with rate limiting."""
        for season in seasons:
            try:
                logger.info(f"Fetching Regular Season stats for season {season}")
                await self.fetch_player_stats(player_id, season, "Regular Season")
                await asyncio.sleep(self.rate_limit_sleep)
                
                logger.info(f"Fetching Playoffs stats for season {season}")
                await self.fetch_player_stats(player_id, season, "Playoffs")
                await asyncio.sleep(self.rate_limit_sleep)
                
            except Exception as e:
                logger.error(f"Failed to collect data for season {season}: {str(e)}")
                continue

async def main():
    """Main function to run the collector."""
    collector = NBACollector()
    
    # Generate all NBA seasons
    all_seasons = generate_seasons()
    logger.info(f"Collecting data for {len(all_seasons)} seasons: {all_seasons[0]} to {all_seasons[-1]}")
    
    # Example: Collect data for LeBron James (2544) for all seasons
    await collector.collect_player_data('2544', all_seasons)

if __name__ == "__main__":
    asyncio.run(main()) 