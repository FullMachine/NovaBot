from typing import Optional, List
from .base import BaseDBModel
from pydantic import Field

class PlayerStats(BaseDBModel):
    points_per_game: float = Field(default=0.0)
    assists_per_game: float = Field(default=0.0)
    rebounds_per_game: float = Field(default=0.0)
    steals_per_game: float = Field(default=0.0)
    blocks_per_game: float = Field(default=0.0)
    field_goal_percentage: float = Field(default=0.0)
    three_point_percentage: float = Field(default=0.0)
    free_throw_percentage: float = Field(default=0.0)
    games_played: int = Field(default=0)
    minutes_per_game: float = Field(default=0.0)

class Player(BaseDBModel):
    name: str = Field(...)
    team: str = Field(...)
    position: str = Field(...)
    jersey_number: Optional[str] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    birth_date: Optional[str] = None
    nationality: Optional[str] = None
    college: Optional[str] = None
    draft_year: Optional[int] = None
    stats: Optional[PlayerStats] = None
    season: str = Field(...) 