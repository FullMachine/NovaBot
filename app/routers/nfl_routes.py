"""
NFL data router for the Nova Sports Data API.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict
from datetime import datetime
from app.services.nfl_service import NFLService
from app.models.nfl import (
    PlayerStats,
    TeamStats,
    GameStats,
    Standings
)

router = APIRouter(prefix="/api/v1/nfl", tags=["NFL"])
nfl_service = NFLService()

@router.get("/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "nfl"}

@router.get("/players/{player_id}", response_model=PlayerStats)
async def get_player_stats(
    player_id: str,
    season: Optional[int] = Query(None, description="NFL season year")
):
    """Get NFL player statistics."""
    try:
        stats = await nfl_service.get_player_stats(player_id, season)
        if not stats:
            raise HTTPException(status_code=404, detail="Player not found")
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teams/{team_id}", response_model=TeamStats)
async def get_team_stats(
    team_id: str,
    season: Optional[int] = Query(None, description="NFL season year")
):
    """Get NFL team statistics."""
    try:
        stats = await nfl_service.get_team_stats(team_id, season)
        if not stats:
            raise HTTPException(status_code=404, detail="Team not found")
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/{game_id}", response_model=GameStats)
async def get_game_stats(game_id: str):
    """Get NFL game statistics."""
    try:
        stats = await nfl_service.get_game_stats(game_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Game not found")
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/standings", response_model=List[Standings])
async def get_standings(
    season: Optional[int] = Query(None, description="NFL season year"),
    week: Optional[int] = Query(None, description="NFL week number")
):
    """Get NFL standings."""
    try:
        standings = await nfl_service.get_standings(season, week)
        return standings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/players/search/{name}")
async def search_players(name: str):
    """Search for NFL players by name."""
    try:
        players = await nfl_service.search_players(name)
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teams/search/{name}")
async def search_teams(name: str):
    """Search for NFL teams by name."""
    try:
        teams = await nfl_service.search_teams(name)
        return teams
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 