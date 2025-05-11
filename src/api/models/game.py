from typing import Optional, List
from .base import BaseDBModel
from pydantic import Field
from datetime import datetime

class GameStats(BaseDBModel):
    points: int = Field(default=0)
    field_goals_made: int = Field(default=0)
    field_goals_attempted: int = Field(default=0)
    three_points_made: int = Field(default=0)
    three_points_attempted: int = Field(default=0)
    free_throws_made: int = Field(default=0)
    free_throws_attempted: int = Field(default=0)
    rebounds: int = Field(default=0)
    assists: int = Field(default=0)
    steals: int = Field(default=0)
    blocks: int = Field(default=0)
    turnovers: int = Field(default=0)
    fouls: int = Field(default=0)

class Game(BaseDBModel):
    home_team: str = Field(...)
    away_team: str = Field(...)
    date: datetime = Field(...)
    season: str = Field(...)
    game_type: str = Field(...)  # regular_season, playoffs, preseason
    status: str = Field(default="scheduled")  # scheduled, live, finished
    home_team_stats: Optional[GameStats] = None
    away_team_stats: Optional[GameStats] = None
    venue: Optional[str] = None
    attendance: Optional[int] = None
    officials: Optional[List[str]] = None 