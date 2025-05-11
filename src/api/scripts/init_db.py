import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def init_db():
    # Connect to MongoDB
    client = AsyncIOMotorClient(os.getenv("DATABASE_URL", "mongodb://localhost:27017/"))
    db = client[os.getenv("DATABASE_NAME", "nova_sports")]
    
    # Sample data
    test_player = {
        "name": "LeBron James",
        "team": "Los Angeles Lakers",
        "position": "Forward",
        "jersey_number": "23",
        "height": "6'9\"",
        "weight": "250 lbs",
        "birth_date": "1984-12-30",
        "nationality": "USA",
        "college": "None",
        "draft_year": 2003,
        "stats": {
            "points_per_game": 27.1,
            "assists_per_game": 7.3,
            "rebounds_per_game": 7.5,
            "steals_per_game": 1.6,
            "blocks_per_game": 0.8,
            "field_goal_percentage": 50.5,
            "three_point_percentage": 34.5,
            "free_throw_percentage": 73.5,
            "games_played": 67,
            "minutes_per_game": 35.5
        },
        "season": "2023-24"
    }

    test_team = {
        "name": "Los Angeles Lakers",
        "city": "Los Angeles",
        "conference": "Western",
        "division": "Pacific",
        "arena": "Crypto.com Arena",
        "head_coach": "Darvin Ham",
        "founded_year": 1947,
        "championships": 17,
        "stats": {
            "wins": 45,
            "losses": 37,
            "points_per_game": 117.5,
            "points_allowed_per_game": 116.8,
            "field_goal_percentage": 49.5,
            "three_point_percentage": 36.5,
            "free_throw_percentage": 78.5,
            "rebounds_per_game": 44.2,
            "assists_per_game": 26.8,
            "steals_per_game": 7.5,
            "blocks_per_game": 5.2
        },
        "season": "2023-24"
    }

    # Insert test data
    await db.players.insert_one(test_player)
    await db.teams.insert_one(test_team)
    
    print("Database initialized with test data!")

if __name__ == "__main__":
    asyncio.run(init_db()) 