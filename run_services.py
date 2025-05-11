"""
Script to run both the API and collector services.
"""
import subprocess
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_api():
    """Run the FastAPI application."""
    subprocess.Popen([
        sys.executable,
        "run.py"
    ])

def run_collector():
    """Run the NBA data collector."""
    subprocess.Popen([
        sys.executable,
        "app/services/nba_collector.py"
    ])

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("logs/api", exist_ok=True)
    os.makedirs("logs/collection", exist_ok=True)
    os.makedirs("logs/errors", exist_ok=True)
    os.makedirs("data/nba/player_stats", exist_ok=True)
    
    # Start both services
    run_api()
    run_collector() 