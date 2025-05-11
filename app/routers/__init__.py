"""
Router initialization for the Nova Sports Data API.
"""
from fastapi import APIRouter

# Create empty routers for each sport
nfl = APIRouter()
nba = APIRouter()
soccer = APIRouter()
baseball = APIRouter()
racing = APIRouter()
esports = APIRouter()
tennis = APIRouter()

# Import route handlers
from . import nfl_routes
from . import nba_routes
from . import soccer_routes
from . import baseball_routes
from . import racing_routes
from . import esports_routes
from . import tennis_routes

# Add routes to routers
nfl.include_router(nfl_routes.router)
# nba.include_router(nba_routes.router)
soccer.include_router(soccer_routes.router)
baseball.include_router(baseball_routes.router)
racing.include_router(racing_routes.router)
esports.include_router(esports_routes.router)
tennis.include_router(tennis_routes.router) 