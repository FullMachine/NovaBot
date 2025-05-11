from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Any
import time
from src.utils.logger import setup_logger

logger = setup_logger("cache", "api.log")

class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, ttl: int = 300):  # 5 minutes default TTL
        super().__init__(app)
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl

    async def dispatch(self, request: Request, call_next):
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)

        # Generate cache key
        cache_key = f"{request.url.path}?{request.url.query}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data["timestamp"] < self.ttl:
                logger.info(f"Cache hit for {cache_key}")
                return cached_data["response"]

        # Process request
        response = await call_next(request)
        
        # Cache response
        self.cache[cache_key] = {
            "timestamp": time.time(),
            "response": response
        }
        logger.info(f"Cached response for {cache_key}")
        
        return response 