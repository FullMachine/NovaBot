import os
import json
import requests
from dotenv import load_dotenv
from ..utils.nba_scraper import get_player_stats

load_dotenv()

class StatsService:
    def __init__(self):
        self.api_keys = {
            'nfl': os.getenv('API_FOOTBALL_KEY'),
            'nba': os.getenv('NBA_API_KEY'),
            # Add more API keys as needed
        }
        self.base_urls = {
            'nba': 'https://www.balldontlie.io/api/v1'
        }

    def get_all_stats(self, sport):
        """Get statistics for all players in a sport"""
        if sport == 'nfl':
            from app.utils.sources.nfl import fetch_all_nfl_player_stats
            return fetch_all_nfl_player_stats()
        # Add more sports handlers as needed
        return []

    def get_player_stats(self, sport, name):
        """Get statistics for a specific player"""
        if sport == 'nfl':
            return self._get_nfl_stats(name)
        elif sport == 'nba':
            return self._get_nba_stats(name)
        # Add more sports handlers as needed
        return {"error": f"Stats not available for {sport}"}

    def _get_nfl_stats(self, name):
        """Get NFL player statistics"""
        api_key = self.api_keys.get('nfl')
        if not api_key:
            return {"error": "NFL API key not configured"}

        url = "https://v3.american-football.api-sports.io/players"
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "v3.american-football.api-sports.io"
        }
        params = {
            "search": name,
            "league": 1,  # NFL
            "season": 2023
        }

        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()

        if "response" not in data or not data["response"]:
            return {"error": "Player not found in API"}

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

    def _get_nba_stats(self, name):
        """Get NBA player statistics using web scraping"""
        try:
            # First check if we already have the stats cached
            cache_file = f"data/nba_stats/{name.lower().replace(' ', '_')}.json"
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    return json.load(f)

            # If not cached, scrape the stats
            stats = get_player_stats(name)
            if stats:
                # Save to cache
                os.makedirs('data/nba_stats', exist_ok=True)
                with open(cache_file, 'w') as f:
                    json.dump(stats, f)
                return stats
            else:
                return {"error": f"Could not find stats for {name}"}
        except Exception as e:
            return {"error": f"Error getting NBA stats: {str(e)}"} 