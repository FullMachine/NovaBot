"""
NBA data models for the Nova Sports Data API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class PlayerStats(BaseModel):
    """NBA player statistics model."""
    player_id: str
    name: str
    team: str
    position: str
    season: int
    last_updated: datetime
    stats: Dict[str, float] = Field(
        description="Player statistics keyed by stat name",
        default_factory=dict
    )
    shooting: Dict[str, float] = Field(
        description="Shooting statistics",
        default_factory=dict
    )
    advanced: Optional[Dict[str, float]] = Field(
        description="Advanced statistics",
        default_factory=dict
    )
    defense: Optional[Dict[str, float]] = Field(
        description="Defensive statistics",
        default_factory=dict
    )

class TeamStats(BaseModel):
    """NBA team statistics model."""
    team_id: str
    name: str
    conference: str
    division: str
    season: int
    last_updated: datetime
    stats: Dict[str, float] = Field(
        description="Team statistics keyed by stat name",
        default_factory=dict
    )
    offense: Dict[str, float] = Field(
        description="Offensive statistics",
        default_factory=dict
    )
    defense: Dict[str, float] = Field(
        description="Defensive statistics",
        default_factory=dict
    )
    advanced: Dict[str, float] = Field(
        description="Advanced statistics",
        default_factory=dict
    )

class GameStats(BaseModel):
    """NBA game statistics model."""
    game_id: str
    season: int
    date: datetime
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    status: str
    quarter: Optional[int]
    time_remaining: Optional[str]
    stats: Dict[str, Dict[str, float]] = Field(
        description="Game statistics by team",
        default_factory=dict
    )
    player_stats: Dict[str, Dict[str, float]] = Field(
        description="Player statistics for this game",
        default_factory=dict
    )

class Standings(BaseModel):
    """NBA standings model."""
    team_id: str
    name: str
    conference: str
    division: str
    wins: int
    losses: int
    win_percentage: float
    games_back: float
    points_for: float
    points_against: float
    point_differential: float
    streak: str
    last_ten: str
    home_record: str
    away_record: str
    conference_record: str
    division_record: str
    playoff_seed: Optional[int]
    playoff_status: Optional[str]

class PlayerGameLog(BaseModel):
    """NBA player game log model."""
    player_id: str
    game_id: str
    date: datetime
    opponent: str
    result: str
    stats: Dict[str, float] = Field(
        description="Game statistics",
        default_factory=dict
    )

class TeamGameLog(BaseModel):
    """NBA team game log model."""
    team_id: str
    game_id: str
    date: datetime
    opponent: str
    result: str
    stats: Dict[str, float] = Field(
        description="Game statistics",
        default_factory=dict
    ) 