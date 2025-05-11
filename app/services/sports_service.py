from typing import Dict, List, Optional
from datetime import datetime
import os
import json
from pathlib import Path

class SportDataService:
    def __init__(self, sport_name: str):
        self.sport_name = sport_name.lower()
        self.data_dir = Path(os.getenv('DATA_DIR', 'data'))
        self.sport_dir = self.data_dir / self.sport_name
        self.cache_dir = Path(os.getenv('CACHE_DIR', 'data/cache'))
        
        # Ensure directories exist
        self.sport_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_player_stats(self, player_id: str) -> Dict:
        """Get player statistics from our data source."""
        stats_file = self.sport_dir / 'player_stats' / f'{player_id}.json'
        if stats_file.exists():
            with open(stats_file) as f:
                return json.load(f)
        return {}

    def get_player_logs(self, player_id: str) -> List[Dict]:
        """Get player game logs from our data source."""
        logs_file = self.sport_dir / 'player_logs' / f'{player_id}.json'
        if logs_file.exists():
            with open(logs_file) as f:
                return json.load(f)
        return []

    def save_player_stats(self, player_id: str, stats: Dict) -> None:
        """Save player statistics to our data source."""
        stats_dir = self.sport_dir / 'player_stats'
        stats_dir.mkdir(exist_ok=True)
        
        with open(stats_dir / f'{player_id}.json', 'w') as f:
            json.dump(stats, f, indent=2)

    def save_player_logs(self, player_id: str, logs: List[Dict]) -> None:
        """Save player game logs to our data source."""
        logs_dir = self.sport_dir / 'player_logs'
        logs_dir.mkdir(exist_ok=True)
        
        with open(logs_dir / f'{player_id}.json', 'w') as f:
            json.dump(logs, f, indent=2)

    def get_all_players(self) -> List[Dict]:
        """Get list of all players in the sport."""
        players_file = self.sport_dir / 'players.json'
        if players_file.exists():
            with open(players_file) as f:
                return json.load(f)
        return []

    def save_players_list(self, players: List[Dict]) -> None:
        """Save list of all players in the sport."""
        with open(self.sport_dir / 'players.json', 'w') as f:
            json.dump(players, f, indent=2)

    def get_team_stats(self, team_id: str) -> Dict:
        """Get team statistics from our data source."""
        stats_file = self.sport_dir / 'team_stats' / f'{team_id}.json'
        if stats_file.exists():
            with open(stats_file) as f:
                return json.load(f)
        return {}

    def save_team_stats(self, team_id: str, stats: Dict) -> None:
        """Save team statistics to our data source."""
        stats_dir = self.sport_dir / 'team_stats'
        stats_dir.mkdir(exist_ok=True)
        
        with open(stats_dir / f'{team_id}.json', 'w') as f:
            json.dump(stats, f, indent=2) 