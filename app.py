from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import os
import openai
import requests
from typing import List, Optional, Dict
from pydantic import BaseModel
from dotenv import load_dotenv
import io
from app.services.nfl_service import NFLService
from app.services.sports_service import SportDataService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Sports Stats API",
    description="API for processing sports statistics and player information",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service dependencies
def get_nfl_service():
    return NFLService()

# Load player names for a sport
def load_player_list(sport: str = "nba") -> List[str]:
    try:
        with open(f"players/{sport}_players.txt", "r") as f:
            return [line.strip().lower() for line in f.readlines()]
    except FileNotFoundError:
        return []

# Save new player to file
def save_new_player(name: str, sport: str = "nba") -> None:
    name = name.strip().lower()
    if not name:
        return
    players = load_player_list(sport)
    if name not in players:
        with open(f"players/{sport}_players.txt", "a") as f:
            f.write(name + "\n")

# Use GPT to verify NBA or NFL player
async def is_valid_player_gpt(name: str, sport: str = "nba") -> bool:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You're a sports assistant. Confirm only real {sport.upper()} player names (past, present, or future)."
                },
                {
                    "role": "user",
                    "content": f"Is '{name}' a real {sport.upper()} player? Just say YES or NO."
                }
            ],
            temperature=0.2
        )
        reply = response['choices'][0]['message']['content'].strip().lower()
        return "yes" in reply
    except Exception as e:
        print("[GPT ERROR]", e)
        return False

# Models
class PlayerResponse(BaseModel):
    players_detected: List[str]
    total_detected: int
    tried_names: List[str]

class PlayerStats(BaseModel):
    player_id: str
    name: str
    stats: Dict
    last_updated: str

class PlayerGameLog(BaseModel):
    player_id: str
    game_date: str
    opponent: str
    stats: Dict

# Routes for NFL
@app.get("/nfl/players/{player_id}/stats", response_model=PlayerStats)
async def get_nfl_player_stats(
    player_id: str,
    nfl_service: NFLService = Depends(get_nfl_service)
):
    """Get NFL player statistics from our own data sources."""
    stats = await nfl_service.get_player_current_stats(player_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Player stats not found")
    return stats

@app.get("/nfl/players/{player_id}/logs")
async def get_nfl_player_logs(
    player_id: str,
    nfl_service: NFLService = Depends(get_nfl_service)
):
    """Get NFL player game logs from our own data sources."""
    logs = await nfl_service.get_player_game_logs(player_id)
    if not logs:
        raise HTTPException(status_code=404, detail="Player logs not found")
    return {"logs": logs}

@app.get("/nfl/players/search")
async def search_nfl_player(
    name: str = Query(..., description="Player name to search for"),
    nfl_service: NFLService = Depends(get_nfl_service)
):
    """Search for an NFL player by name."""
    player = await nfl_service.search_player(name)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@app.get("/nfl/teams/{team_id}/stats")
async def get_nfl_team_stats(
    team_id: str,
    nfl_service: NFLService = Depends(get_nfl_service)
):
    """Get NFL team statistics from our own data sources."""
    stats = await nfl_service.get_team_season_stats(team_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Team stats not found")
    return stats

@app.post("/upload", response_model=PlayerResponse)
async def upload(
    screenshot: UploadFile = File(...),
    sport: str = Query("nba", regex="^(nba|nfl)$")
):
    try:
        contents = await screenshot.read()
        image = Image.open(io.BytesIO(contents))
        raw_text = pytesseract.image_to_string(image)
        words = raw_text.split('\n')
        tried_names = [w.strip() for w in words if w.strip()]

        player_list = load_player_list(sport)
        detected = []

        for name in tried_names:
            name_clean = name.lower().strip()
            if name_clean in player_list:
                detected.append(name.title())
            elif await is_valid_player_gpt(name_clean, sport):
                detected.append(name.title())
                save_new_player(name_clean, sport)

        if not detected:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "No players found or valid stats fetched",
                    "tried_names": tried_names
                }
            )

        return PlayerResponse(
            players_detected=detected,
            total_detected=len(detected),
            tried_names=tried_names
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/players/{sport}", response_model=dict)
async def get_players(sport: str = Query(..., regex="^(nba|nfl)$")):
    try:
        players = load_player_list(sport)
        return {"players": players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/players/nfl/stats")
async def get_all_nfl_stats():
    try:
        from utils.sources import nfl
        players = nfl.fetch_all_nfl_player_stats()
        return {"players": players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats/nfl")
async def get_nfl_stats(name: str = Query(..., description="Player name")):
    api_key = os.getenv("API_FOOTBALL_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API Football key not configured")

    url = "https://v3.american-football.api-sports.io/players"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "v3.american-football.api-sports.io"
    }
    params = {
        "search": name,
        "league": 1,     # NFL
        "season": 2023
    }

    try:
        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()

        if "response" not in data or not data["response"]:
            raise HTTPException(status_code=404, detail="Player not found in API")

        player_info = data["response"][0]
        player_id = player_info["player"]["id"]

        # Get stats
        stats_url = "https://v3.american-football.api-sports.io/players/statistics"
        stats_params = {
            "player": player_id,
            "league": 1,
            "season": 2023
        }

        stats_resp = requests.get(stats_url, headers=headers, params=stats_params)
        stats_data = stats_resp.json()

        return {
            "player": name,
            "player_id": player_id,
            "stats": stats_data.get("response", {})
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)