"""
Pydantic schemas for team-related data.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class TeamBase(BaseModel):
    """Base team information."""
    name: str = Field(..., description="Team's full name")
    abbreviation: str = Field(..., description="Team's abbreviation")
    city: str = Field(..., description="Team's city")
    conference: str = Field(..., description="Team's conference (East/West)")
    division: str = Field(..., description="Team's division")

class TeamStats(BaseModel):
    """Team statistics."""
    wins: int = Field(..., description="Number of wins")
    losses: int = Field(..., description="Number of losses")
    win_percentage: float = Field(..., description="Win percentage")
    points_per_game: float = Field(..., description="Points per game")
    points_allowed: float = Field(..., description="Points allowed per game")
    rebounds_per_game: float = Field(..., description="Rebounds per game")
    assists_per_game: float = Field(..., description="Assists per game")
    net_rating: float = Field(..., description="Net rating")

class TeamResponse(TeamBase):
    """Complete team information with statistics."""
    id: str = Field(..., description="Team's unique identifier")
    stats: Optional[TeamStats] = Field(None, description="Team statistics")
    roster: List[str] = Field(default_factory=list, description="List of player IDs on the team") 