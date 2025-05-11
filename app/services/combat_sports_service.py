from typing import Dict, List, Optional
import json
from pathlib import Path
from datetime import datetime
import logging
from .sports_service import SportDataService

logger = logging.getLogger(__name__)

class CombatSportsService(SportDataService):
    SPORTS = {
        'ufc': 'Ultimate Fighting Championship',
        'boxing': 'Professional Boxing'
    }

    WEIGHT_CLASSES = {
        'ufc': {
            'flyweight': 'Flyweight',
            'bantamweight': 'Bantamweight',
            'featherweight': 'Featherweight',
            'lightweight': 'Lightweight',
            'welterweight': 'Welterweight',
            'middleweight': 'Middleweight',
            'light_heavyweight': 'Light Heavyweight',
            'heavyweight': 'Heavyweight',
            'w_strawweight': "Women's Strawweight",
            'w_flyweight': "Women's Flyweight",
            'w_bantamweight': "Women's Bantamweight",
            'w_featherweight': "Women's Featherweight"
        },
        'boxing': {
            'minimumweight': 'Minimumweight',
            'light_flyweight': 'Light Flyweight',
            'flyweight': 'Flyweight',
            'super_flyweight': 'Super Flyweight',
            'bantamweight': 'Bantamweight',
            'super_bantamweight': 'Super Bantamweight',
            'featherweight': 'Featherweight',
            'super_featherweight': 'Super Featherweight',
            'lightweight': 'Lightweight',
            'super_lightweight': 'Super Lightweight',
            'welterweight': 'Welterweight',
            'super_welterweight': 'Super Welterweight',
            'middleweight': 'Middleweight',
            'super_middleweight': 'Super Middleweight',
            'light_heavyweight': 'Light Heavyweight',
            'cruiserweight': 'Cruiserweight',
            'heavyweight': 'Heavyweight'
        }
    }

    def __init__(self, sport_id: str):
        super().__init__(f'combat/{sport_id}')
        self.sport_id = sport_id
        self.sport_name = self.SPORTS.get(sport_id, 'Unknown Combat Sport')
        self.weight_classes = self.WEIGHT_CLASSES.get(sport_id, {})

    async def get_fighter_stats(self, fighter_id: str) -> Dict:
        """Get fighter statistics."""
        try:
            stats = self.get_player_stats(fighter_id)  # Reuse player stats storage
            if not stats:
                await self.collect_fighter_stats(fighter_id)
                stats = self.get_player_stats(fighter_id)
            return stats
        except Exception as e:
            logger.error(f"Error getting {self.sport_name} fighter stats: {e}")
            return {}

    async def collect_fighter_stats(self, fighter_id: str) -> None:
        """Collect fighter statistics."""
        try:
            stats = {
                "fighter_id": fighter_id,
                "sport": self.sport_name,
                "last_updated": datetime.now().isoformat(),
                "stats": self._get_sport_specific_stats()
            }
            
            # Implement actual data collection here
            
            self.save_player_stats(fighter_id, stats)  # Reuse player stats storage
            
        except Exception as e:
            logger.error(f"Error collecting {self.sport_name} fighter stats: {e}")
            raise

    def _get_sport_specific_stats(self) -> Dict:
        """Get sport-specific stats structure."""
        if self.sport_id == 'ufc':
            return {
                "general": {
                    "record": {
                        "wins": 0,
                        "losses": 0,
                        "draws": 0,
                        "no_contests": 0
                    },
                    "weight_class": "",
                    "ranking": 0,
                    "title_holder": False
                },
                "performance": {
                    "knockouts": 0,
                    "submissions": 0,
                    "decisions": 0,
                    "striking_accuracy": 0.0,
                    "takedown_accuracy": 0.0,
                    "striking_defense": 0.0,
                    "takedown_defense": 0.0
                },
                "striking": {
                    "strikes_landed_per_min": 0.0,
                    "strikes_absorbed_per_min": 0.0,
                    "significant_strikes_landed": 0,
                    "significant_strikes_attempted": 0,
                    "head_strikes_landed": 0,
                    "body_strikes_landed": 0,
                    "leg_strikes_landed": 0
                },
                "grappling": {
                    "takedowns_landed": 0,
                    "takedowns_attempted": 0,
                    "submission_attempts": 0,
                    "reversals": 0,
                    "control_time_seconds": 0
                }
            }
        elif self.sport_id == 'boxing':
            return {
                "general": {
                    "record": {
                        "wins": 0,
                        "losses": 0,
                        "draws": 0,
                        "no_contests": 0
                    },
                    "weight_class": "",
                    "ranking": {
                        "wbc": 0,
                        "wba": 0,
                        "ibf": 0,
                        "wbo": 0
                    },
                    "titles": []
                },
                "performance": {
                    "knockouts": 0,
                    "knockout_percentage": 0.0,
                    "rounds_boxed": 0,
                    "average_fight_length": 0.0
                },
                "striking": {
                    "punches_landed_per_round": 0.0,
                    "punches_thrown_per_round": 0.0,
                    "accuracy": 0.0,
                    "power_punches_landed": 0,
                    "power_punches_thrown": 0,
                    "jabs_landed": 0,
                    "jabs_thrown": 0
                }
            }
        return {}

    async def get_event_data(self, event_id: str) -> Dict:
        """Get event data including fight card and results."""
        try:
            event_file = self.sport_dir / 'events' / f'{event_id}.json'
            if event_file.exists():
                with open(event_file) as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error getting event data: {e}")
            return {}

    async def get_rankings(self, weight_class: Optional[str] = None) -> Dict:
        """Get rankings, optionally filtered by weight class."""
        try:
            rankings_file = self.sport_dir / 'rankings.json'
            if rankings_file.exists():
                with open(rankings_file) as f:
                    rankings = json.load(f)
                    if weight_class:
                        return {
                            weight_class: rankings.get(weight_class, {})
                        }
                    return rankings
            return {}
        except Exception as e:
            logger.error(f"Error getting rankings: {e}")
            return {}

    async def get_upcoming_events(self) -> List[Dict]:
        """Get upcoming events."""
        try:
            events_file = self.sport_dir / 'upcoming_events.json'
            if events_file.exists():
                with open(events_file) as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error getting upcoming events: {e}")
            return []

    async def get_fight_history(self, fighter_id: str) -> List[Dict]:
        """Get fighter's fight history."""
        try:
            history_file = self.sport_dir / 'fight_history' / f'{fighter_id}.json'
            if history_file.exists():
                with open(history_file) as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error getting fight history: {e}")
            return [] 