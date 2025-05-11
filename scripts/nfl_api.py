from fastapi import FastAPI, Query
from typing import List, Optional
import sqlite3

app = FastAPI()
DB_FILE = 'nfl_stats.db'

def query_db(query, params=()):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/players/{player}/stats")
def get_player_stats(player: str, year: Optional[int] = None):
    if year:
        rows = query_db("SELECT * FROM game_logs WHERE player = ? AND year = ?", (player, year))
    else:
        rows = query_db("SELECT * FROM game_logs WHERE player = ?", (player,))
    return {"player": player, "stats": rows}

@app.get("/stats")
def get_stats(year: Optional[int] = None, team: Optional[str] = None, limit: int = 100):
    query = "SELECT * FROM game_logs WHERE 1=1"
    params = []
    if year:
        query += " AND year = ?"
        params.append(year)
    if team:
        query += " AND opponent = ?"
        params.append(team)
    query += " LIMIT ?"
    params.append(limit)
    rows = query_db(query, tuple(params))
    return {"results": rows}

@app.get("/health_report")
def health_report():
    # Example: count missing or suspicious files
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM game_logs WHERE touchdowns IS NULL OR touchdowns = ''")
    missing_td = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM game_logs WHERE yards IS NULL OR yards = ''")
    missing_yards = cur.fetchone()[0]
    conn.close()
    return {
        "missing_touchdowns": missing_td,
        "missing_yards": missing_yards
    } 