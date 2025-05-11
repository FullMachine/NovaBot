"""
Pydantic schemas for game-related data.
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class TeamGameStats(BaseModel):
    """Team statistics for a specific game."""
    team_id: str = Field(..., description="Team's unique identifier")
    points: int = Field(..., description="Total points scored")
    field_goals_made: int = Field(..., description="Field goals made")
    field_goals_attempted: int = Field(..., description="Field goals attempted")
    field_goal_percentage: float = Field(..., description="Field goal percentage")
    three_pointers_made: int = Field(..., description="Three pointers made")
    three_pointers_attempted: int = Field(..., description="Three pointers attempted")
    three_point_percentage: float = Field(..., description="Three point percentage")
    free_throws_made: int = Field(..., description="Free throws made")
    free_throws_attempted: int = Field(..., description="Free throws attempted")
    free_throw_percentage: float = Field(..., description="Free throw percentage")
    rebounds: int = Field(..., description="Total rebounds")
    assists: int = Field(..., description="Total assists")
    steals: int = Field(..., description="Total steals")
    blocks: int = Field(..., description="Total blocks")
    turnovers: int = Field(..., description="Total turnovers")

class PlayerGameStats(BaseModel):
    """Player statistics for a specific game."""
    player_id: str = Field(..., description="Player's unique identifier")
    minutes_played: str = Field(..., description="Minutes played")
    points: int = Field(..., description="Points scored")
    rebounds: int = Field(..., description="Total rebounds")
    assists: int = Field(..., description="Total assists")
    steals: int = Field(..., description="Total steals")
    blocks: int = Field(..., description="Total blocks")
    turnovers: int = Field(..., description="Total turnovers")
    field_goals_made: int = Field(..., description="Field goals made")
    field_goals_attempted: int = Field(..., description="Field goals attempted")
    three_pointers_made: int = Field(..., description="Three pointers made")
    three_pointers_attempted: int = Field(..., description="Three pointers attempted")
    free_throws_made: int = Field(..., description="Free throws made")
    free_throws_attempted: int = Field(..., description="Free throws attempted")

class GameResponse(BaseModel):
    """Complete game information with team and player statistics."""
    id: str = Field(..., description="Game's unique identifier")
    date: datetime = Field(..., description="Game date and time")
    season: str = Field(..., description="Season (e.g., '2024-25')")
    home_team_id: str = Field(..., description="Home team's unique identifier")
    away_team_id: str = Field(..., description="Away team's unique identifier")
    status: str = Field(..., description="Game status (scheduled, live, final)")
    home_team_score: Optional[int] = Field(None, description="Home team's score")
    away_team_score: Optional[int] = Field(None, description="Away team's score")
    home_team_stats: Optional[TeamGameStats] = Field(None, description="Home team's statistics")
    away_team_stats: Optional[TeamGameStats] = Field(None, description="Away team's statistics")
    player_stats: List[PlayerGameStats] = Field(default_factory=list, description="Individual player statistics") 