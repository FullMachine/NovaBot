import logging
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
from pathlib import Path
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class DataCollector:
    def __init__(self, sport: str, data_dir: str = "data"):
        self.sport = sport.lower()
        self.data_dir = Path(data_dir) / self.sport
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up logging
        self.logger = logging.getLogger(f"{self.sport}_collector")
        self.logger.setLevel(logging.INFO)
        
        # Create handlers
        fh = logging.FileHandler(self.data_dir / f"{self.sport}_collection.log")
        fh.setLevel(logging.INFO)
        
        # Create formatters and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        
        # Add handlers to the logger
        self.logger.addHandler(fh)
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 3.0  # seconds
        
    def _rate_limit(self):
        """Implement rate limiting to avoid overwhelming APIs."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        self.last_request_time = time.time()
        
    def _make_request(self, url: str, headers: Optional[Dict] = None, params: Optional[Dict] = None) -> Optional[requests.Response]:
        """Make a request to the API with rate limiting and exponential backoff."""
        max_retries = 5
        base_delay = 3  # Base delay of 3 seconds
        
        for attempt in range(max_retries):
            try:
                # Wait to respect rate limit
                self._rate_limit()
                
                # Add debug logging
                self.logger.info(f"Making request to: {url}")
                self.logger.info(f"Headers: {headers}")
                self.logger.info(f"Params: {params}")
                
                # Make request
                response = requests.get(url, headers=headers, params=params)
                
                # Add response logging
                self.logger.info(f"Response status code: {response.status_code}")
                self.logger.info(f"Response headers: {response.headers}")
                
                # Check if we hit rate limit (429) or server error (5xx)
                if response.status_code == 429 or (response.status_code >= 500 and response.status_code < 600):
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    self.logger.warning(f"Rate limit or server error. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    continue
                    
                # Check other error responses
                if response.status_code != 200:
                    self.logger.error(f"Response text: {response.text}")
                    response.raise_for_status()
                    
                return response
                
            except Exception as e:
                delay = base_delay * (2 ** attempt)
                self.logger.error(f"Request failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    self.logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    self.logger.error("Max retries reached")
                    return None
        
    def collect_player_data(self, player_id: str) -> Optional[Dict]:
        """Collect detailed player statistics and information."""
        try:
            # TODO: Implement sport-specific data collection
            self.logger.info(f"Collecting data for player {player_id}")
            return None
        except Exception as e:
            self.logger.error(f"Error collecting player data: {str(e)}")
            return None
            
    def collect_team_data(self, team_id: str) -> Optional[Dict]:
        """Collect team statistics and information."""
        try:
            # TODO: Implement sport-specific data collection
            self.logger.info(f"Collecting data for team {team_id}")
            return None
        except Exception as e:
            self.logger.error(f"Error collecting team data: {str(e)}")
            return None
            
    def collect_game_data(self, game_id: str) -> Optional[Dict]:
        """Collect game statistics and information."""
        try:
            # TODO: Implement sport-specific data collection
            self.logger.info(f"Collecting data for game {game_id}")
            return None
        except Exception as e:
            self.logger.error(f"Error collecting game data: {str(e)}")
            return None
            
    def save_data(self, data: Dict, data_type: str, identifier: str) -> bool:
        """Save collected data to JSON file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{data_type}_{identifier}_{timestamp}.json"
            filepath = self.data_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
                
            self.logger.info(f"Saved {data_type} data for {identifier}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
            return False
            
    def load_data(self, data_type: str, identifier: str) -> Optional[Dict]:
        """Load previously collected data."""
        try:
            # Find the most recent file for this data type and identifier
            pattern = f"{data_type}_{identifier}_*.json"
            files = list(self.data_dir.glob(pattern))
            
            if not files:
                return None
                
            latest_file = max(files, key=lambda x: x.stat().st_mtime)
            
            with open(latest_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            return None

class NBADataCollector(DataCollector):
    def __init__(self):
        super().__init__("nba")
        self.base_url = "https://stats.nba.com/stats"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.nba.com',
            'Referer': 'https://www.nba.com/',
            'x-nba-stats-origin': 'stats',
            'x-nba-stats-token': 'true'
        }
        self.min_request_interval = 3.0  # Increase rate limit to 3 seconds
        
    def get_all_players(self) -> List[Dict]:
        """Get a list of all NBA players."""
        try:
            url = f"{self.base_url}/commonallplayers"
            params = {
                'LeagueID': '00',  # NBA
                'Season': '2023-24',  # Current season
                'IsOnlyCurrentSeason': '0'  # Get all players, not just current season
            }
            
            self.logger.info("Fetching all NBA players")
            response = self._make_request(url, headers=self.headers, params=params)
            
            if not response:
                self.logger.error("Failed to get all players")
                return []
                
            data = response.json()
            if 'resultSets' not in data or not data['resultSets']:
                self.logger.error("No resultSets found in response")
                return []
                
            players = []
            headers = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']
            
            for row in rows:
                player = {}
                for i, header in enumerate(headers):
                    player[header] = row[i]
                players.append(player)
                
            self.logger.info(f"Retrieved {len(players)} players")
            return players
            
        except Exception as e:
            self.logger.error(f"Error getting all players: {str(e)}")
            return []
            
    def verify_player_data(self, player_id: str, collected_data: Dict) -> Dict:
        """Verify collected data against NBA.com"""
        url = f"{self.base_url}/playergamelog"
        params = {
            'PlayerID': player_id,
            'Season': '2023-24',
            'SeasonType': 'Regular Season'
        }
        
        try:
            response = self._make_request(url, headers=self.headers, params=params)
            official_data = response.json()
            
            # Compare stats
            our_games = len(collected_data['stats']['Regular Season'])
            official_games = len(official_data['resultSets'][0]['rowSet'])
            
            verification_result = {
                'player_id': player_id,
                'player_name': collected_data['stats']['Regular Season'][0]['PLAYER_NAME'],
                'our_games': our_games,
                'official_games': official_games,
                'matches': our_games == official_games,
                'verification_time': datetime.now().isoformat()
            }
            
            # Log verification result
            self.logger.info(f"Verification for {verification_result['player_name']}: {our_games} games collected, {official_games} games official")
            
            # Save verification result
            verification_file = f"{self.data_dir}/verification_{player_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(verification_file, 'w') as f:
                json.dump(verification_result, f, indent=2)
            
            return verification_result
        except Exception as e:
            self.logger.error(f"Error verifying player {player_id}: {str(e)}")
            return {
                'player_id': player_id,
                'error': str(e),
                'verification_time': datetime.now().isoformat()
            }

    def collect_player_data(self, player_id: str, seasons: Optional[List[str]] = None) -> Optional[Dict]:
        """Collect NBA player statistics and information for specified seasons."""
        try:
            self.logger.info(f"Collecting NBA data for player {player_id}")
            
            # Define the different season types to collect
            season_types = {
                'Regular Season': 'Regular Season',
                'Pre Season': 'Pre Season',
                'Playoffs': 'Playoffs'
            }
            
            # If no seasons specified, get current season
            if not seasons:
                current_year = datetime.now().year
                current_month = datetime.now().month
                # If we're in the first half of the year, use previous season
                if current_month < 7:
                    seasons = [f"{current_year-1}-{str(current_year)[-2:]}"]
                else:
                    seasons = [f"{current_year}-{str(current_year+1)[-2:]}"]
            
            all_stats = {}
            
            for season in seasons:
                season_stats = {}
                for season_name, season_type in season_types.items():
                    url = f"{self.base_url}/playergamelogs"
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
                    
                    self.logger.info(f"Fetching {season_name} stats for season {season} from {url}")
                    response = self._make_request(url, headers=self.headers, params=params)
                    
                    if not response:
                        self.logger.warning(f"Failed to get {season_name} stats for season {season}")
                        continue
                    
                    try:
                        data = response.json()
                        if 'resultSets' not in data:
                            self.logger.warning(f"No resultSets found in response for {season_name} season {season}")
                            continue
                            
                        # Get the headers and rows from the response
                        headers = data['resultSets'][0]['headers']
                        rows = data['resultSets'][0]['rowSet']
                        
                        # Convert rows to list of dictionaries
                        stats = []
                        for row in rows:
                            game_stats = {}
                            for i, header in enumerate(headers):
                                game_stats[header] = row[i]
                            stats.append(game_stats)
                        
                        if stats:
                            season_stats[season_name] = stats
                            
                    except ValueError as e:
                        self.logger.error(f"Error parsing JSON response: {str(e)}")
                        continue
                
                if season_stats:
                    all_stats[season] = season_stats
            
            if not all_stats:
                self.logger.error("Failed to collect any stats")
                return None
            
            # Save the data
            player_data = {
                'player_id': player_id,
                'stats': all_stats,
                'last_updated': datetime.now().isoformat()
            }
            
            self.save_data(player_data, 'player', player_id)
            
            # Verify the data
            verification_result = self.verify_player_data(player_id, player_data)
            
            # If verification failed, log it but don't stop the process
            if 'error' in verification_result or not verification_result['matches']:
                self.logger.warning(f"Verification issues for player {player_id}: {verification_result}")
            
            return player_data
            
        except Exception as e:
            self.logger.error(f"Error collecting NBA player data: {str(e)}")
            return None
            
    def __del__(self):
        """Clean up Selenium driver when object is destroyed."""
        if hasattr(self, 'driver'):
            self.driver.quit()

class NFLDataCollector(DataCollector):
    def __init__(self):
        super().__init__("nfl")
        
    def collect_player_data(self, player_id: str) -> Optional[Dict]:
        """Collect NFL player statistics and information."""
        try:
            # TODO: Implement NFL-specific data collection
            self.logger.info(f"Collecting NFL data for player {player_id}")
            return None
        except Exception as e:
            self.logger.error(f"Error collecting NFL player data: {str(e)}")
            return None

class MLBDataCollector(DataCollector):
    def __init__(self):
        super().__init__("mlb")
        
    def collect_player_data(self, player_id: str) -> Optional[Dict]:
        """Collect MLB player statistics and information."""
        try:
            # TODO: Implement MLB-specific data collection
            self.logger.info(f"Collecting MLB data for player {player_id}")
            return None
        except Exception as e:
            self.logger.error(f"Error collecting MLB player data: {str(e)}")
            return None 