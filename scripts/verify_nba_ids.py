"""
Script to verify and update NBA player IDs against official sources.
Uses both NBA.com stats API and web scraping as fallback.
"""
import aiohttp
import asyncio
import json
import logging
import os
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/collection/nba_id_verification.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('nba_id_verification')

class NBAPlayerVerifier:
    def __init__(self):
        self.session = None
        self.verified_players = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.nba.com',
            'Accept': 'application/json'
        }
        
    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
            
    async def close(self):
        if self.session:
            await self.session.close()
            
    async def verify_player_id(self, player_name: str, player_id: str) -> Optional[str]:
        """Verify a player ID against NBA.com stats API."""
        try:
            # Try NBA stats API first
            url = f"https://stats.nba.com/stats/commonplayerinfo?PlayerID={player_id}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['resultSets'][0]['rowSet']:
                        return player_id
                    
            # If API fails, try web scraping as fallback
            search_url = f"https://www.nba.com/players/{player_name.lower().replace(' ', '-')}"
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    # Look for player ID in page source
                    player_data = soup.find('script', {'id': '__NEXT_DATA__'})
                    if player_data:
                        data = json.loads(player_data.string)
                        # Extract player ID from page data
                        return str(data['props']['pageProps']['player']['playerId'])
                        
        except Exception as e:
            logger.error(f"Error verifying {player_name} (ID: {player_id}): {str(e)}")
            
        return None

    async def load_existing_ids(self) -> Dict[str, str]:
        """Load existing player IDs from file."""
        try:
            with open('data/players/nba_player_ids.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("No existing player IDs file found")
            return {}

    async def verify_all_players(self):
        """Verify all player IDs and update the file."""
        await self.init_session()
        existing_ids = await self.load_existing_ids()
        
        for name, player_id in existing_ids.items():
            verified_id = await self.verify_player_id(name, player_id)
            if verified_id:
                self.verified_players[name] = verified_id
            else:
                logger.warning(f"Could not verify ID for {name}")
                
        # Save verified IDs
        os.makedirs('data/players', exist_ok=True)
        with open('data/players/nba_player_ids_verified.json', 'w') as f:
            json.dump(self.verified_players, f, indent=2)
            
        logger.info(f"Verified {len(self.verified_players)} player IDs")
        
async def main():
    verifier = NBAPlayerVerifier()
    try:
        await verifier.verify_all_players()
    finally:
        await verifier.close()

if __name__ == "__main__":
    asyncio.run(main()) 