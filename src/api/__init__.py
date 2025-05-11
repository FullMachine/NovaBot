"""
API package initialization.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .middleware.request_logger import RequestLoggerMiddleware

# Create FastAPI app
app = FastAPI(
    title="Sports Analytics API",
    description="API for accessing sports statistics and analytics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logger middleware
app.add_middleware(RequestLoggerMiddleware)

@app.get("/")
async def root():
    return {"message": "Welcome to Sports Analytics API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import other modules after app is created
from .config.database import Database
from .middleware.rate_limiter import RateLimiterMiddleware
from .middleware.cache import CacheMiddleware
from .middleware.auth import AuthMiddleware
from .routers import players, teams, games, auth

# Add custom middlewares
app.add_middleware(RateLimiterMiddleware, max_requests=100, window_seconds=60)
app.add_middleware(CacheMiddleware, ttl_seconds=300)
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(players.router, prefix="/api/v1/players", tags=["players"])
app.include_router(teams.router, prefix="/api/v1/teams", tags=["teams"])
app.include_router(games.router, prefix="/api/v1/games", tags=["games"])

@app.on_event("startup")
async def startup():
    await Database.connect_db()

@app.on_event("shutdown")
async def shutdown():
    await Database.close_db() 