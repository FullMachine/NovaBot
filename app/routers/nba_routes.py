"""
NBA data router for the Nova Sports Data API.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict
from datetime import datetime
from app.services.nba_service import NBAService
from app.models.nba import (
    PlayerStats,
    TeamStats,
    GameStats,
    Standings
)
import os
import json
import glob

print(">>> nba_routes.py LOADED:", __file__)

router = APIRouter(prefix="/api/v1/nba", tags=["NBA"])
nba_service = NBAService()

# Path to player IDs JSON file
PLAYER_IDS_PATH = os.path.join(os.getenv("DATA_DIR", "data"), "players", "nba_player_ids.json")

# Hardcoded NBA teams and IDs (example subset)
NBA_TEAMS = [
    {"name": "Atlanta Hawks", "id": "1610612737"},
    {"name": "Boston Celtics", "id": "1610612738"},
    {"name": "Brooklyn Nets", "id": "1610612751"},
    {"name": "Charlotte Hornets", "id": "1610612766"},
    {"name": "Chicago Bulls", "id": "1610612741"},
    {"name": "Cleveland Cavaliers", "id": "1610612739"},
    {"name": "Dallas Mavericks", "id": "1610612742"},
    {"name": "Denver Nuggets", "id": "1610612743"},
    {"name": "Detroit Pistons", "id": "1610612765"},
    {"name": "Golden State Warriors", "id": "1610612744"},
    {"name": "Houston Rockets", "id": "1610612745"},
    {"name": "Indiana Pacers", "id": "1610612754"},
    {"name": "LA Clippers", "id": "1610612746"},
    {"name": "Los Angeles Lakers", "id": "1610612747"},
    {"name": "Memphis Grizzlies", "id": "1610612763"},
    {"name": "Miami Heat", "id": "1610612748"},
    {"name": "Milwaukee Bucks", "id": "1610612749"},
    {"name": "Minnesota Timberwolves", "id": "1610612750"},
    {"name": "New Orleans Pelicans", "id": "1610612740"},
    {"name": "New York Knicks", "id": "1610612752"},
    {"name": "Oklahoma City Thunder", "id": "1610612760"},
    {"name": "Orlando Magic", "id": "1610612753"},
    {"name": "Philadelphia 76ers", "id": "1610612755"},
    {"name": "Phoenix Suns", "id": "1610612756"},
    {"name": "Portland Trail Blazers", "id": "1610612757"},
    {"name": "Sacramento Kings", "id": "1610612758"},
    {"name": "San Antonio Spurs", "id": "1610612759"},
    {"name": "Toronto Raptors", "id": "1610612761"},
    {"name": "Utah Jazz", "id": "1610612762"},
    {"name": "Washington Wizards", "id": "1610612764"},
]

@router.get("/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {"status": "healthy", "service": "nba"}

@router.get("/players/search")
async def search_players_by_name(query: Optional[str] = None):
    """Search for NBA players by (partial) name, or return all if no query."""
    try:
        with open(PLAYER_IDS_PATH, "r") as f:
            players = json.load(f)
        # players is a dict: {name: id}
        if query:
            results = [
                {"name": name, "id": pid}
                for name, pid in players.items()
                if query.lower() in name.lower()
            ]
        else:
            results = [
                {"name": name, "id": pid}
                for name, pid in players.items()
            ]
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/players/{player_id}", response_model=PlayerStats)
async def get_player_stats(
    player_id: str,
    season: Optional[int] = Query(None, description="NBA season year")
):
    """Get NBA player statistics."""
    try:
        stats = await nba_service.get_player_stats(player_id, season)
        if not stats:
            raise HTTPException(status_code=404, detail="Player not found")
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teams/search")
async def search_teams_by_name(query: str):
    """Search for NBA teams by (partial) name."""
    results = [team for team in NBA_TEAMS if query.lower() in team["name"].lower()]
    return {"results": results}

@router.get("/teams/{team_id}", response_model=TeamStats)
async def get_team_stats(
    team_id: str,
    season: Optional[int] = Query(None, description="NBA season year")
):
    """Get NBA team statistics."""
    try:
        stats = await nba_service.get_team_stats(team_id, season)
        if not stats:
            raise HTTPException(status_code=404, detail="Team not found")
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/{game_id}", response_model=GameStats)
async def get_game_stats(game_id: str):
    """Get NBA game statistics."""
    try:
        stats = await nba_service.get_game_stats(game_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Game not found")
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/standings", response_model=List[Standings])
async def get_standings(
    season: Optional[int] = Query(None, description="NBA season year")
):
    """Get NBA standings."""
    try:
        standings = await nba_service.get_standings(season)
        return standings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/players/{player_id}/summary")
async def player_stats_summary(player_id: str, season: str):
    """Get a summary of a player's stats for a given season."""
    try:
        # Path to the stats file
        stats_path = os.path.join(
            os.getenv("DATA_DIR", "data"),
            "nba", "player_stats", season, f"{player_id}_regular_season.json"
        )
        if not os.path.exists(stats_path):
            raise HTTPException(status_code=404, detail="Stats file not found for player/season")
        with open(stats_path, "r") as f:
            data = json.load(f)
        # Extract stats from rowSet
        result_set = data.get("resultSets", [{}])[0]
        headers = result_set.get("headers", [])
        rows = result_set.get("rowSet", [])
        if not rows:
            return {"summary": {}, "message": "No data for this player/season."}
        # Sum up numeric stats
        summary = {h: 0 for h in headers if h not in ("SEASON_YEAR", "PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "TEAM_NAME", "GAME_ID", "GAME_DATE", "MATCHUP", "WL")}
        for row in rows:
            for i, h in enumerate(headers):
                if h in summary and isinstance(row[i], (int, float)):
                    summary[h] += row[i]
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compare_players")
async def compare_players(
    player1_id: str = Query(..., description="First player's NBA ID"),
    player2_id: str = Query(..., description="Second player's NBA ID"),
    season: int = Query(..., description="NBA season year (e.g., 2023)")
):
    """Compare two NBA players' stats for a given season."""
    try:
        result = await nba_service.compare_players(player1_id, player2_id, season)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 