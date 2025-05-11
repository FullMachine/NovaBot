from typing import Dict, List, Optional
import json
from pathlib import Path
from datetime import datetime
import logging
from .sports_service import SportDataService

logger = logging.getLogger(__name__)

class BaseballService(SportDataService):
    LEAGUES = {
        'kbo': 'Korea Baseball Organization',
        'npb': 'Nippon Professional Baseball',
        'bbl': 'Big Bash League'
    }

    def __init__(self, league_id: str):
        super().__init__(f'baseball/{league_id}')
        self.league_id = league_id
        self.league_name = self.LEAGUES.get(league_id, 'Unknown League')

    async def get_player_current_stats(self, player_id: str) -> Dict:
        """Get current season stats for a baseball player."""
        try:
            stats = self.get_player_stats(player_id)
            if not stats:
                await self.collect_player_stats(player_id)
                stats = self.get_player_stats(player_id)
            return stats
        except Exception as e:
            logger.error(f"Error getting {self.league_name} player stats: {e}")
            return {}

    async def collect_player_stats(self, player_id: str) -> None:
        """Collect baseball player statistics."""
        try:
            stats = {
                "player_id": player_id,
                "league": self.league_name,
                "last_updated": datetime.now().isoformat(),
                "season": datetime.now().year,
                "stats": self._get_league_specific_stats()
            }
            
            self.save_player_stats(player_id, stats)
            
        except Exception as e:
            logger.error(f"Error collecting {self.league_name} player stats: {e}")
            raise

    def _get_league_specific_stats(self) -> Dict:
        """Get league-specific stats structure."""
        batting_stats = {
            "batting": {
                "games": 0,
                "plate_appearances": 0,
                "at_bats": 0,
                "runs": 0,
                "hits": 0,
                "doubles": 0,
                "triples": 0,
                "home_runs": 0,
                "rbi": 0,
                "stolen_bases": 0,
                "caught_stealing": 0,
                "walks": 0,
                "strikeouts": 0,
                "batting_average": 0.0,
                "on_base_percentage": 0.0,
                "slugging_percentage": 0.0,
                "ops": 0.0
            }
        }

        pitching_stats = {
            "pitching": {
                "games": 0,
                "games_started": 0,
                "complete_games": 0,
                "shutouts": 0,
                "wins": 0,
                "losses": 0,
                "saves": 0,
                "innings_pitched": 0.0,
                "hits_allowed": 0,
                "runs_allowed": 0,
                "earned_runs": 0,
                "home_runs_allowed": 0,
                "walks": 0,
                "strikeouts": 0,
                "era": 0.0,
                "whip": 0.0,
                "strikeouts_per_nine": 0.0
            }
        }

        fielding_stats = {
            "fielding": {
                "games": 0,
                "games_started": 0,
                "innings": 0.0,
                "total_chances": 0,
                "putouts": 0,
                "assists": 0,
                "errors": 0,
                "double_plays": 0,
                "fielding_percentage": 0.0
            }
        }

        # Combine all stats
        return {
            **batting_stats,
            **pitching_stats,
            **fielding_stats
        }

    async def get_team_stats(self, team_id: str) -> Dict:
        """Get team statistics."""
        try:
            stats = super().get_team_stats(team_id)
            if not stats:
                await self.collect_team_stats(team_id)
                stats = super().get_team_stats(team_id)
            return stats
        except Exception as e:
            logger.error(f"Error getting {self.league_name} team stats: {e}")
            return {}

    async def collect_team_stats(self, team_id: str) -> None:
        """Collect team statistics."""
        try:
            stats = {
                "team_id": team_id,
                "league": self.league_name,
                "last_updated": datetime.now().isoformat(),
                "season": datetime.now().year,
                "stats": {
                    "overall": {
                        "games_played": 0,
                        "wins": 0,
                        "losses": 0,
                        "win_percentage": 0.0,
                        "games_back": 0.0,
                        "streak": "",
                        "last_ten": ""
                    },
                    "home": {
                        "wins": 0,
                        "losses": 0,
                        "win_percentage": 0.0
                    },
                    "away": {
                        "wins": 0,
                        "losses": 0,
                        "win_percentage": 0.0
                    },
                    "batting": {
                        "runs": 0,
                        "hits": 0,
                        "home_runs": 0,
                        "batting_average": 0.0,
                        "on_base_percentage": 0.0,
                        "slugging_percentage": 0.0
                    },
                    "pitching": {
                        "era": 0.0,
                        "strikeouts": 0,
                        "saves": 0,
                        "whip": 0.0
                    }
                }
            }
            
            self.save_team_stats(team_id, stats)
            
        except Exception as e:
            logger.error(f"Error collecting {self.league_name} team stats: {e}")
            raise

    async def get_standings(self) -> List[Dict]:
        """Get current league standings."""
        try:
            standings_file = self.sport_dir / 'standings.json'
            if standings_file.exists():
                with open(standings_file) as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error getting standings: {e}")
            return []

    async def get_schedule(self, team_id: Optional[str] = None) -> List[Dict]:
        """Get schedule (all games or by team)."""
        try:
            if team_id:
                schedule_file = self.sport_dir / 'team_schedules' / f'{team_id}.json'
            else:
                schedule_file = self.sport_dir / 'schedule.json'
            
            if schedule_file.exists():
                with open(schedule_file) as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error getting schedule: {e}")
            return [] 