from typing import Dict, List, Optional
import json
from pathlib import Path
from datetime import datetime
import logging
from .sports_service import SportDataService

logger = logging.getLogger(__name__)

class RacingService(SportDataService):
    RACING_TYPES = {
        'f1': 'Formula 1',
        'nascar': 'NASCAR'
    }

    def __init__(self, racing_type: str):
        super().__init__(f'racing/{racing_type}')
        self.racing_type = racing_type
        self.series_name = self.RACING_TYPES.get(racing_type, 'Unknown Series')

    async def get_driver_stats(self, driver_id: str) -> Dict:
        """Get driver statistics."""
        try:
            stats = self.get_player_stats(driver_id)  # Reuse player stats storage
            if not stats:
                await self.collect_driver_stats(driver_id)
                stats = self.get_player_stats(driver_id)
            return stats
        except Exception as e:
            logger.error(f"Error getting {self.series_name} driver stats: {e}")
            return {}

    async def collect_driver_stats(self, driver_id: str) -> None:
        """Collect driver statistics."""
        try:
            stats = {
                "driver_id": driver_id,
                "series": self.series_name,
                "last_updated": datetime.now().isoformat(),
                "season": datetime.now().year,
                "stats": self._get_series_specific_stats()
            }
            
            self.save_player_stats(driver_id, stats)
            
        except Exception as e:
            logger.error(f"Error collecting {self.series_name} driver stats: {e}")
            raise

    def _get_series_specific_stats(self) -> Dict:
        """Get series-specific stats structure."""
        if self.racing_type == 'f1':
            return {
                "career": {
                    "championships": 0,
                    "race_wins": 0,
                    "podiums": 0,
                    "pole_positions": 0,
                    "fastest_laps": 0,
                    "points": 0
                },
                "current_season": {
                    "position": 0,
                    "points": 0,
                    "wins": 0,
                    "podiums": 0,
                    "pole_positions": 0,
                    "fastest_laps": 0,
                    "races_completed": 0,
                    "dnfs": 0  # Did Not Finish
                },
                "qualifying": {
                    "best_position": 0,
                    "average_position": 0.0
                },
                "race": {
                    "best_position": 0,
                    "average_position": 0.0,
                    "laps_led": 0,
                    "laps_completed": 0
                }
            }
        elif self.racing_type == 'nascar':
            return {
                "career": {
                    "championships": 0,
                    "race_wins": 0,
                    "top_5": 0,
                    "top_10": 0,
                    "pole_positions": 0,
                    "points": 0
                },
                "current_season": {
                    "position": 0,
                    "points": 0,
                    "playoff_points": 0,
                    "wins": 0,
                    "top_5": 0,
                    "top_10": 0,
                    "pole_positions": 0,
                    "races_completed": 0,
                    "dnfs": 0
                },
                "qualifying": {
                    "best_position": 0,
                    "average_position": 0.0
                },
                "race": {
                    "best_position": 0,
                    "average_position": 0.0,
                    "laps_led": 0,
                    "laps_completed": 0,
                    "lead_lap_finishes": 0
                }
            }
        return {}

    async def get_team_stats(self, team_id: str) -> Dict:
        """Get team statistics."""
        try:
            stats = super().get_team_stats(team_id)
            if not stats:
                await self.collect_team_stats(team_id)
                stats = super().get_team_stats(team_id)
            return stats
        except Exception as e:
            logger.error(f"Error getting {self.series_name} team stats: {e}")
            return {}

    async def get_race_results(self, race_id: str) -> Dict:
        """Get race results."""
        try:
            results_file = self.sport_dir / 'races' / f'{race_id}.json'
            if results_file.exists():
                with open(results_file) as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error getting race results: {e}")
            return {}

    async def get_championship_standings(self) -> Dict:
        """Get current championship standings."""
        try:
            standings_file = self.sport_dir / 'standings.json'
            if standings_file.exists():
                with open(standings_file) as f:
                    return json.load(f)
            return {
                "drivers": [],
                "constructors": []
            }
        except Exception as e:
            logger.error(f"Error getting championship standings: {e}")
            return {} 