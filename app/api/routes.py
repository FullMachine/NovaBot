from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import JSONResponse
from app.services.player_service import PlayerService
from app.services.ocr_service import OCRService
from app.services.stats_service import StatsService

player_service = PlayerService()
ocr_service = OCRService()
stats_service = StatsService()

router = APIRouter()

@router.post("/upload")
async def upload(screenshot: UploadFile = File(...), sport: str = Query("nba")):
    """Upload screenshot for player detection"""
    try:
        result = ocr_service.process_screenshot(screenshot.file, sport)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/players/{sport}")
async def get_players(sport: str):
    """Get player list for a specific sport"""
    try:
        players = player_service.get_players(sport)
        return {"players": players}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/players/{sport}/stats")
async def get_all_stats(sport: str):
    """Get statistics for all players in a sport"""
    try:
        stats = stats_service.get_all_stats(sport)
        return {"players": stats}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/stats/{sport}")
async def get_player_stats(sport: str, name: str = Query(None)):
    """Get statistics for a specific player"""
    if not name:
        return JSONResponse(content={"error": "Missing ?name= query param"}, status_code=400)
    try:
        stats = stats_service.get_player_stats(sport, name)
        return stats
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500) 