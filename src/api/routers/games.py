"""
Router for game-related endpoints.
"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, HTTPException, Query
from src.api.schemas.game import GameResponse
from src.utils.logger import setup_logger

# Set up logging
logger = setup_logger("games_router", "api.log")

# Create router
router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[GameResponse])
async def get_games(
    start_date: Optional[date] = Query(None, description="Start date for games (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date for games (YYYY-MM-DD)"),
    team_id: Optional[str] = Query(None, description="Filter by team ID"),
    season: Optional[str] = Query(None, description="Filter by season (e.g., '2024-25')"),
    status: Optional[str] = Query(None, description="Filter by game status (scheduled, live, final)")
):
    """
    Get a list of games with optional filtering.
    """
    try:
        # TODO: Implement actual data fetching from database/storage
        return []
    except Exception as e:
        logger.error(f"Error fetching games: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/today", response_model=List[GameResponse])
async def get_today_games():
    """
    Get all games scheduled for today.
    """
    try:
        # TODO: Implement actual data fetching
        return []
    except Exception as e:
        logger.error(f"Error fetching today's games: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/live", response_model=List[GameResponse])
async def get_live_games():
    """
    Get all currently live games.
    """
    try:
        # TODO: Implement actual data fetching
        return []
    except Exception as e:
        logger.error(f"Error fetching live games: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{game_id}", response_model=GameResponse)
async def get_game(game_id: str):
    """
    Get detailed information about a specific game.
    """
    try:
        # TODO: Implement actual game data fetching
        raise HTTPException(status_code=404, detail="Game not found")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching game {game_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{game_id}/boxscore", response_model=GameResponse)
async def get_game_boxscore(game_id: str):
    """
    Get the complete boxscore for a specific game.
    """
    try:
        # TODO: Implement actual boxscore fetching
        raise HTTPException(status_code=404, detail="Game boxscore not found")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching boxscore for game {game_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") 