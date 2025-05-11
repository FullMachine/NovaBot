"""
Configuration settings for the NBA Data Analytics Platform.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "nba"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"

# Data collection settings
COLLECTION_INTERVAL = int(os.getenv("COLLECTION_INTERVAL", "600"))  # 10 minutes
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "60"))  # 1 minute

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# NBA API settings
NBA_API_TIMEOUT = int(os.getenv("NBA_API_TIMEOUT", "30"))
NBA_API_DELAY = float(os.getenv("NBA_API_DELAY", "0.6"))  # Delay between API calls 