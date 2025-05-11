"""
Main FastAPI application for the Nova Sports Data API.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import os
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import pathlib

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(os.getenv("LOG_DIR", "logs"), "api.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Nova Sports Data API",
    description="API for accessing sports data across multiple leagues and sports",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

# Import routers after app creation to avoid circular imports
from app.routers.nfl_routes import router as nfl_router
from app.routers.nba_routes import router as nba_router
from app.routers.soccer_routes import router as soccer_router
from app.routers.baseball_routes import router as baseball_router
from app.routers.racing_routes import router as racing_router
from app.routers.esports_routes import router as esports_router
from app.routers.tennis_routes import router as tennis_router

# Include routers
app.include_router(nfl_router)
app.include_router(nba_router)
app.include_router(soccer_router)
app.include_router(baseball_router)
app.include_router(racing_router)
app.include_router(esports_router)
app.include_router(tennis_router)

# Serve static files for favicon and apple-touch-icon
static_dir = pathlib.Path(__file__).parent.parent.resolve()
app.mount("/", StaticFiles(directory=static_dir, html=False), name="static")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail, "status_code": exc.status_code})

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(status_code=500, content={"error": "Internal server error", "status_code": 500})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True if os.getenv("ENVIRONMENT") == "development" else False,
        workers=int(os.getenv("API_WORKERS", 1))
    ) 