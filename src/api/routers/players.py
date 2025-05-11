"""
Router for player-related endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from src.api.schemas.player import PlayerResponse
from src.utils.logger import setup_logger
from src.api.services.nba_service import NBAService
import os
import json
from fastapi.responses import JSONResponse
import glob
import csv

# Set up logging
logger = setup_logger("players_router", "api.log")

# Create router
router = APIRouter(
    tags=["players"],
    responses={404: {"description": "Not found"}},
)

nba_service = NBAService()

@router.get(
    "/",
    response_model=List[PlayerResponse],
    summary="List Players",
    description="Retrieve a list of players with optional filtering by name and position, and support for pagination via limit and offset."
)
async def get_players(
    limit: int = Query(50, description="Number of players to return (pagination limit)"),
    offset: int = Query(0, description="Number of players to skip (pagination offset)"),
    search: Optional[str] = Query(None, description="Search players by name (case-insensitive)"),
    position: Optional[str] = Query(None, description="Filter players by position (e.g., 'Guard', 'Forward', etc.)")
):
    """
    Get a list of players with optional filtering and pagination.
    - **limit**: Number of players to return (default: 50)
    - **offset**: Number of players to skip (default: 0)
    - **search**: Search players by name
    - **position**: Filter by player position
    """
    try:
        mock_players = [
            {
                "name": "LeBron James",
                "id": "2544",
                "position": "Forward",
                "height": "6 ft 9 in",
                "weight": "250",
                "birth_date": "1984-12-30",
                "college": None,
                "career_stats": {
                    "points": 27.2,
                    "rebounds": 7.5,
                    "assists": 7.3,
                    "steals": 1.5,
                    "blocks": 0.8,
                    "field_goal_percentage": 50.5,
                    "three_point_percentage": 34.6,
                    "free_throw_percentage": 73.4
                },
                "season_stats": []
            },
            {
                "name": "Stephen Curry",
                "id": "201939",
                "position": "Guard",
                "height": "6 ft 2 in",
                "weight": "185",
                "birth_date": "1988-03-14",
                "college": None,
                "career_stats": {
                    "points": 24.8,
                    "rebounds": 4.7,
                    "assists": 6.4,
                    "steals": 1.6,
                    "blocks": 0.2,
                    "field_goal_percentage": 47.5,
                    "three_point_percentage": 42.8,
                    "free_throw_percentage": 91.0
                },
                "season_stats": []
            },
            {
                "name": "Kevin Durant",
                "id": "201142",
                "position": "Forward",
                "height": "6 ft 10 in",
                "weight": "240",
                "birth_date": "1988-09-29",
                "college": None,
                "career_stats": {
                    "points": 27.3,
                    "rebounds": 7.0,
                    "assists": 4.3,
                    "steals": 1.1,
                    "blocks": 1.1,
                    "field_goal_percentage": 50.1,
                    "three_point_percentage": 38.7,
                    "free_throw_percentage": 88.6
                },
                "season_stats": []
            },
            {
                "name": "Giannis Antetokounmpo",
                "id": "203507",
                "position": "Forward",
                "height": "7 ft 0 in",
                "weight": "242",
                "birth_date": "1994-12-06",
                "college": None,
                "career_stats": {
                    "points": 23.4,
                    "rebounds": 9.8,
                    "assists": 4.7,
                    "steals": 1.1,
                    "blocks": 1.3,
                    "field_goal_percentage": 54.7,
                    "three_point_percentage": 28.7,
                    "free_throw_percentage": 71.2
                },
                "season_stats": []
            },
        ]
        filtered = mock_players
        if search:
            filtered = [p for p in filtered if search.lower() in p["name"].lower()]
        if position:
            filtered = [p for p in filtered if p["position"].lower() == position.lower()]
        paginated = filtered[offset:offset+limit]
        # Convert to PlayerResponse objects
        paginated_models = [PlayerResponse(**p) for p in paginated]
        logger.info(f"Returning {len(paginated_models)} players: {paginated_models}")
        return paginated_models
    except Exception as e:
        logger.error(f"Error fetching players: {str(e)}")
        return []

@router.get("/search", response_model=List[PlayerResponse])
async def search_players(
    limit: int = Query(10000, description="Number of players to return (pagination limit)"),
    offset: int = Query(0, description="Number of players to skip (pagination offset)"),
    search: Optional[str] = Query(None, description="Search players by name (case-insensitive, partial match)"),
    position: Optional[str] = Query(None, description="Filter players by position (e.g., 'Guard', 'Forward', etc.)"),
    team: Optional[str] = Query(None, description="Filter players by team abbreviation (e.g., 'CHI', 'LAL', etc.)"),
    season: Optional[str] = Query("2023-24", description="NBA season (e.g., '2023-24')")
):
    logger.info("search_players endpoint called")
    players = []
    files = glob.glob(f"data/nba/player_stats/{season}/*_regular_season.json")
    for file in files:
        try:
            with open(file, "r") as f:
                data = json.load(f)
            result_sets = data.get("resultSets", [])
            if not result_sets or not result_sets[0].get("rowSet"):
                logger.warning(f"No rows found in file: {file}")
                continue
            rows = result_sets[0]["rowSet"]
            if not rows:
                logger.warning(f"No rows found in file: {file}")
                continue
            row = rows[0]
            headers = result_sets[0]["headers"]
            player_dict = dict(zip(headers, row))
            player_team = player_dict.get("TEAM_ABBREVIATION", "")
            player = PlayerResponse(
                id=str(player_dict.get("PLAYER_ID", "")),
                name=player_dict.get("PLAYER_NAME", "Unknown"),
                position="",  # Position not in file, leave blank or try to infer
                height="",
                weight="",
                birth_date="",
                college=None,
                career_stats=None,
                season_stats=[]
            )
            player_dict_out = player.dict()
            player_dict_out["team"] = player_team
            players.append(player_dict_out)
        except Exception as e:
            logger.error(f"Error loading player from {file}: {e}")
            continue
    # Filter by search if needed
    if search:
        players = [p for p in players if search.lower() in p["name"].lower()]
        logger.info(f"Filtered players by search='{search}', found {len(players)} matches.")
        return players[:limit] if players else []
    # Filter by team if needed
    if team:
        players = [p for p in players if p["team"].lower() == team.lower()]
    paginated = players[offset:offset+limit]
    logger.info(f"Returning {len(paginated)} real players from data files (season={season}, team={team}).")
    return paginated if paginated else []

@router.get("/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: str):
    """
    Get detailed information about a specific player.
    """
    try:
        # TODO: Implement actual player data fetching
        # This is a placeholder that raises a 404
        raise HTTPException(status_code=404, detail="Player not found")
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error fetching player {player_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{player_id}/stats", response_model=PlayerResponse)
async def get_player_stats(
    player_id: str,
    season: Optional[str] = Query(None, description="Filter by season (e.g., '2024-25')")
):
    """
    Get statistics for a specific player, optionally filtered by season.
    """
    # Use 2023-24 as default season if not specified
    season = season or "2023-24"
    stats_path = f"data/nba/player_stats/{season}/{player_id}_regular_season.json"
    info_path = f"data/players/{player_id}.json"

    # Try to load stats file
    if os.path.exists(stats_path):
        with open(stats_path, "r") as f:
            stats_data = json.load(f)
        # Try to get player info (name, etc.)
        if os.path.exists(info_path):
            with open(info_path, "r") as f:
                info_data = json.load(f)
        else:
            # Fallback: try to get name from stats file
            result_sets = stats_data.get("resultSets", [])
            if result_sets and result_sets[0]["rowSet"]:
                player_name = result_sets[0]["rowSet"][0][2]
            else:
                player_name = "Unknown"
            info_data = {
                "name": player_name,
                "position": "Unknown",
                "height": "Unknown",
                "weight": "Unknown",
                "birth_date": "Unknown",
                "college": None
            }
        # Build PlayerResponse
        response = {
            "id": player_id,
            "name": info_data["name"],
            "position": info_data.get("position", "Unknown"),
            "height": info_data.get("height", "Unknown"),
            "weight": info_data.get("weight", "Unknown"),
            "birth_date": info_data.get("birth_date", "Unknown"),
            "college": info_data.get("college"),
            "career_stats": None,  # Not implemented yet
            "season_stats": stats_data.get("resultSets", [])
        }
        return response
    else:
        # No stats found, return friendly message
        return {
            "id": player_id,
            "name": "No data available",
            "position": "",
            "height": "",
            "weight": "",
            "birth_date": "",
            "college": None,
            "career_stats": None,
            "season_stats": []
        }

@router.get("/nba/players_collected/", summary="List all collected NBA players for a season")
async def get_collected_nba_players(season: str = "2023-24"):
    """Return a summary of all collected NBA players for a given season."""
    try:
        players = nba_service.summarize_collected_players(season)
        logger.info(f"Returning {len(players)} players for season {season}")
        return players if players is not None else []
    except Exception as e:
        logger.error(f"Error in get_collected_nba_players: {e}")
        return []

@router.get("/nba/seasons/", summary="List all available NBA seasons")
async def get_nba_seasons():
    """Return a list of all available NBA seasons."""
    try:
        return nba_service.list_seasons()
    except Exception as e:
        logger.error(f"Error in get_nba_seasons: {e}")
        return []

@router.get("/test_player", response_model=PlayerResponse)
async def test_player():
    """Return a single valid PlayerResponse object for debugging."""
    player = {
        "name": "Test Player",
        "id": "9999",
        "position": "Guard",
        "height": "6 ft 3 in",
        "weight": "200",
        "birth_date": "1990-01-01",
        "college": "Test University",
        "career_stats": {
            "points": 10.0,
            "rebounds": 5.0,
            "assists": 7.0,
            "steals": 1.0,
            "blocks": 0.5,
            "field_goal_percentage": 45.0,
            "three_point_percentage": 35.0,
            "free_throw_percentage": 80.0
        },
        "season_stats": []
    }
    logger.info(f"Returning test player: {player}")
    return player

@router.get("/verification_report")
async def get_verification_report(only_discrepancies: bool = False):
    """Return all players and their verification discrepancies from the CSV report. If only_discrepancies is true, only return players with issues."""
    report_file = "verify_nba_players_full_report.csv"
    fixed_file = "fixed_players.json"
    fixed_players = set()
    if os.path.exists(fixed_file):
        import json
        with open(fixed_file, "r") as f:
            fixed_players = set(json.load(f))
    players = []
    try:
        with open(report_file, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                discrepancies = row.get("Discrepancies", "")
                is_fixed = (discrepancies == "{}") or (row.get("Local ID", "") in fixed_players)
                if only_discrepancies and (discrepancies == "{}" or is_fixed):
                    continue
                players.append({
                    "player_name": row.get("Player Name", ""),
                    "local_id": row.get("Local ID", ""),
                    "nba_name": row.get("NBA.com Name", ""),
                    "nba_id": row.get("NBA.com ID", ""),
                    "nba_team": row.get("NBA.com Team", ""),
                    "nba_position": row.get("NBA.com Position", ""),
                    "discrepancies": discrepancies,
                    "fixed": is_fixed
                })
    except Exception as e:
        logger.error(f"Error reading verification report: {e}")
        return []
    return players 