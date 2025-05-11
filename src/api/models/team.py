from typing import Optional, List
from .base import BaseDBModel
from pydantic import Field

class TeamStats(BaseDBModel):
    wins: int = Field(default=0)
    losses: int = Field(default=0)
    points_per_game: float = Field(default=0.0)
    points_allowed_per_game: float = Field(default=0.0)
    field_goal_percentage: float = Field(default=0.0)
    three_point_percentage: float = Field(default=0.0)
    free_throw_percentage: float = Field(default=0.0)
    rebounds_per_game: float = Field(default=0.0)
    assists_per_game: float = Field(default=0.0)
    steals_per_game: float = Field(default=0.0)
    blocks_per_game: float = Field(default=0.0)

class Team(BaseDBModel):
    name: str = Field(...)
    city: str = Field(...)
    conference: str = Field(...)
    division: str = Field(...)
    arena: Optional[str] = None
    head_coach: Optional[str] = None
    founded_year: Optional[int] = None
    championships: Optional[int] = Field(default=0)
    stats: Optional[TeamStats] = None
    season: str = Field(...) 