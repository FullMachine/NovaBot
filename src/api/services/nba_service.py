"""
Service layer for NBA data operations.
"""
from typing import List, Optional, Dict, Any
import json
from pathlib import Path
from datetime import datetime, date
from src.utils.logger import setup_logger
from src.utils.config import DATA_DIR

logger = setup_logger("nba_service", "api.log")

class NBAService:
    def __init__(self):
        self.data_dir = DATA_DIR
        self.players_dir = self.data_dir / "players"
        self.teams_dir = self.data_dir / "teams"
        self.games_dir = self.data_dir / "games"

    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON data from file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {file_path}: {str(e)}")
            return {}

    def get_players(self, limit: int = 50, offset: int = 0, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of players with optional filtering."""
        players = []
        try:
            for file in self.players_dir.glob("*.json"):
                data = self._load_json(file)
                if not data:
                    continue
                
                if search and search.lower() not in data.get("info", {}).get("name", "").lower():
                    continue
                
                players.append({
                    "id": file.stem,
                    **data
                })
            
            # Apply pagination
            return players[offset:offset + limit]
        except Exception as e:
            logger.error(f"Error fetching players: {str(e)}")
            return []

    def get_player(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get player details by ID."""
        file_path = self.players_dir / f"{player_id}.json"
        data = self._load_json(file_path)
        if data:
            return {"id": player_id, **data}
        return None

    def get_teams(self, conference: Optional[str] = None, division: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get list of teams with optional filtering."""
        teams = []
        try:
            for file in self.teams_dir.glob("*.json"):
                data = self._load_json(file)
                if not data:
                    continue
                
                if conference and data.get("conference", "").lower() != conference.lower():
                    continue
                if division and data.get("division", "").lower() != division.lower():
                    continue
                
                teams.append({
                    "id": file.stem,
                    **data
                })
            return teams
        except Exception as e:
            logger.error(f"Error fetching teams: {str(e)}")
            return []

    def get_team(self, team_id: str) -> Optional[Dict[str, Any]]:
        """Get team details by ID."""
        file_path = self.teams_dir / f"{team_id}.json"
        data = self._load_json(file_path)
        if data:
            return {"id": team_id, **data}
        return None

    def get_games(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        team_id: Optional[str] = None,
        season: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of games with optional filtering."""
        games = []
        try:
            for file in self.games_dir.glob("*.json"):
                data = self._load_json(file)
                if not data:
                    continue

                game_date = datetime.fromisoformat(data.get("date")).date()
                if start_date and game_date < start_date:
                    continue
                if end_date and game_date > end_date:
                    continue
                if team_id and team_id not in [data.get("home_team_id"), data.get("away_team_id")]:
                    continue
                if season and data.get("season") != season:
                    continue
                if status and data.get("status", "").lower() != status.lower():
                    continue

                games.append({
                    "id": file.stem,
                    **data
                })
            return games
        except Exception as e:
            logger.error(f"Error fetching games: {str(e)}")
            return []

    def get_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """Get game details by ID."""
        file_path = self.games_dir / f"{game_id}.json"
        data = self._load_json(file_path)
        if data:
            return {"id": game_id, **data}
        return None

    def get_live_games(self) -> List[Dict[str, Any]]:
        """Get all currently live games."""
        return self.get_games(status="live")

    def get_today_games(self) -> List[Dict[str, Any]]:
        """Get all games scheduled for today."""
        today = date.today()
        return self.get_games(start_date=today, end_date=today)

    def summarize_collected_players(self, season: str = "2023-24") -> list[dict]:
        """Summarize all collected players for a given season (default: 2023-24)."""
        stats_dir = Path(self.data_dir) / "player_stats" / season
        summary = {}
        for file in stats_dir.glob("*_regular_season.json"):
            try:
                with open(file, "r") as f:
                    data = json.load(f)
                # Extract player ID from filename
                player_id = str(file.stem.split("_")[0])
                # Extract player name from first row in rowSet
                result_sets = data.get("resultSets", [])
                if result_sets and result_sets[0]["rowSet"]:
                    player_name = str(result_sets[0]["rowSet"][0][2])
                else:
                    player_name = None
                summary[player_id] = player_name
            except Exception as e:
                logger.error(f"Error reading {file}: {e}")
                continue  # Skip this file and continue
        result = [{"id": str(pid), "name": (str(pname) if pname is not None else None)} for pid, pname in summary.items()]
        logger.info(f"summarize_collected_players returning: {result[:3]}... total={len(result)}")
        return result

    def list_seasons(self) -> list[str]:
        """List all available NBA seasons (directory names in player_stats)."""
        stats_dir = Path(self.data_dir) / "player_stats"
        return sorted([d.name for d in stats_dir.iterdir() if d.is_dir()], reverse=True) 