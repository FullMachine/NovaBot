"""
Base service class for all sports data services.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging
import os
import json
import aiohttp
import asyncio
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class BaseService:
    """Base service class for sports data collection and processing."""
    
    def __init__(self):
        """Initialize the base service."""
        self.data_dir = os.getenv("DATA_DIR", "data")
        self.cache_dir = os.getenv("CACHE_DIR", "data/cache")
        # Strip any comments from environment variables
        cache_expiry_str = os.getenv("CACHE_EXPIRY", "3600").split("#")[0].strip()
        self.cache_expiry = int(cache_expiry_str)
        
    async def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Make an HTTP request with rate limiting and error handling."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 429:
                        retry_after = int(response.headers.get("Retry-After", 60))
                        logger.warning(f"Rate limit hit, waiting {retry_after} seconds")
                        await asyncio.sleep(retry_after)
                        return await self._make_request(url, params)
                    
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"HTTP request failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch data")
            
    def _get_cache_path(self, key: str) -> str:
        """Get the cache file path for a given key."""
        return os.path.join(self.cache_dir, f"{key}.json")
        
    async def _get_cached_data(self, key: str) -> Optional[Dict]:
        """Get data from cache if available and not expired."""
        cache_path = self._get_cache_path(key)
        try:
            if not os.path.exists(cache_path):
                return None
                
            with open(cache_path, "r") as f:
                cached = json.load(f)
                
            if datetime.now().timestamp() - cached["timestamp"] > self.cache_expiry:
                return None
                
            return cached["data"]
        except Exception as e:
            logger.error(f"Cache read error: {str(e)}")
            return None
            
    async def _cache_data(self, key: str, data: Any) -> None:
        """Cache data with timestamp."""
        cache_path = self._get_cache_path(key)
        try:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "w") as f:
                json.dump({
                    "timestamp": datetime.now().timestamp(),
                    "data": data
                }, f)
        except Exception as e:
            logger.error(f"Cache write error: {str(e)}")
            
    def _get_data_path(self, sport: str, category: str, filename: str) -> str:
        """Get the data file path for persistent storage."""
        return os.path.join(self.data_dir, sport, category, filename)
        
    async def _save_data(self, sport: str, category: str, filename: str, data: Any) -> None:
        """Save data to persistent storage."""
        file_path = self._get_data_path(sport, category, filename)
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Data save error: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save data")
            
    async def _load_data(self, sport: str, category: str, filename: str) -> Optional[Dict]:
        """Load data from persistent storage."""
        file_path = self._get_data_path(sport, category, filename)
        try:
            if not os.path.exists(file_path):
                return None
                
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Data load error: {str(e)}")
            return None
            
    async def _update_data(self, sport: str, category: str, filename: str, data: Dict) -> None:
        """Update existing data in persistent storage."""
        existing_data = await self._load_data(sport, category, filename)
        if existing_data:
            existing_data.update(data)
            await self._save_data(sport, category, filename, existing_data)
        else:
            await self._save_data(sport, category, filename, data) 