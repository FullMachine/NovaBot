"""
Pydantic schemas for player-related data.
"""
from typing import List, Optional
from pydantic import BaseModel, Field

class PlayerBase(BaseModel):
    """Base player information."""
    name: str = Field(..., description="Player's full name")
    position: str = Field(..., description="Player's position")
    height: str = Field(..., description="Player's height")
    weight: str = Field(..., description="Player's weight")
    birth_date: str = Field(..., description="Player's birth date")
    college: Optional[str] = Field(None, description="Player's college")

class PlayerStats(BaseModel):
    """Player statistics."""
    points: float = Field(..., description="Points per game")
    rebounds: float = Field(..., description="Rebounds per game")
    assists: float = Field(..., description="Assists per game")
    steals: float = Field(..., description="Steals per game")
    blocks: float = Field(..., description="Blocks per game")
    field_goal_percentage: float = Field(..., description="Field goal percentage")
    three_point_percentage: Optional[float] = Field(None, description="Three-point percentage")
    free_throw_percentage: float = Field(..., description="Free throw percentage")

class PlayerResponse(PlayerBase):
    """Complete player information with statistics."""
    id: str = Field(..., description="Player's unique identifier")
    career_stats: Optional[PlayerStats] = Field(None, description="Career statistics")
    season_stats: List[PlayerStats] = Field(default_factory=list, description="Season-by-season statistics") 