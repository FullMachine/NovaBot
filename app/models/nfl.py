"""
NFL data models for the Nova Sports Data API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class PlayerStats(BaseModel):
    """NFL player statistics model."""
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
    passing: Optional[Dict[str, float]] = Field(
        description="Passing statistics",
        default_factory=dict
    )
    rushing: Optional[Dict[str, float]] = Field(
        description="Rushing statistics",
        default_factory=dict
    )
    receiving: Optional[Dict[str, float]] = Field(
        description="Receiving statistics",
        default_factory=dict
    )
    defense: Optional[Dict[str, float]] = Field(
        description="Defensive statistics",
        default_factory=dict
    )
    kicking: Optional[Dict[str, float]] = Field(
        description="Kicking statistics",
        default_factory=dict
    )

class TeamStats(BaseModel):
    """NFL team statistics model."""
    team_id: str
    name: str
    division: str
    conference: str
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
    special_teams: Dict[str, float] = Field(
        description="Special teams statistics",
        default_factory=dict
    )

class GameStats(BaseModel):
    """NFL game statistics model."""
    game_id: str
    season: int
    week: int
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
    scoring_plays: List[Dict] = Field(
        description="List of scoring plays",
        default_factory=list
    )

class Standings(BaseModel):
    """NFL standings model."""
    team_id: str
    name: str
    division: str
    conference: str
    wins: int
    losses: int
    ties: int
    win_percentage: float
    points_for: int
    points_against: int
    point_differential: int
    division_record: str
    conference_record: str
    streak: str
    last_five: str
    playoff_seed: Optional[int]
    playoff_status: Optional[str]

class PlayerGameLog(BaseModel):
    """NFL player game log model."""
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
    """NFL team game log model."""
    team_id: str
    game_id: str
    date: datetime
    opponent: str
    result: str
    stats: Dict[str, float] = Field(
        description="Game statistics",
        default_factory=dict
    ) 