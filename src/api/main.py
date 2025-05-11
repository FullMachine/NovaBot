"""
Main FastAPI application for the NBA Data Analytics Platform.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.utils.logger import setup_logger
from src.utils.config import API_HOST, API_PORT
from src.api.routers import players, teams, games, auth
from src.api.middleware.rate_limiter import RateLimiterMiddleware
from src.api.middleware.cache import CacheMiddleware
from src.api.middleware.request_logger import RequestLoggerMiddleware
from src.api.middleware.auth import AuthMiddleware
from src.api.config.database import Database
from bson import ObjectId
from fastapi.encoders import ENCODERS_BY_TYPE
from .config.settings import settings
from .config.database import get_database, close_database

# Configure ObjectId encoding
ENCODERS_BY_TYPE[ObjectId] = str

# Set up logging
logger = setup_logger("api", "api.log")

# Create FastAPI app
app = FastAPI(
    title="Sports Analytics API",
    description="API for accessing sports statistics and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logger middleware
app.add_middleware(RequestLoggerMiddleware)

# Add rate limiter middleware
app.add_middleware(RateLimiterMiddleware, max_requests=100, time_window=60)

# Add cache middleware
app.add_middleware(CacheMiddleware, ttl=300)

# Add auth middleware
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(players.router, prefix="/api/v1/nba/players", tags=["players"])
app.include_router(teams.router, prefix="/api/v1/teams", tags=["teams"])
app.include_router(games.router, prefix="/api/v1/games", tags=["games"])

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Sports Analytics API",
        "version": "1.0.0",
        "status": "active",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "auth": "/api/v1/auth",
            "players": "/api/v1/nba/players",
            "teams": "/api/v1/teams",
            "games": "/api/v1/games",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        server_info = await app.mongodb.command("serverInfo")
        return {
            "status": "healthy",
            "database_connected": True,
            "database_version": server_info.get("version", "unknown")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database_connected": False,
            "error": str(e)
        }

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Sports Analytics API")
    app.mongodb = await get_database()
    logger.info("API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Sports Analytics API")
    await close_database(app.mongodb)
    logger.info("API shutting down...")

def custom_openapi():
    """Customize OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Sports Analytics API",
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    
    # Add custom documentation
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.nba.com/assets/logos/nba-logoman-word-white.svg"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    ) 