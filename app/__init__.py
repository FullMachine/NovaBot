"""
Nova Sports Data API package.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure data directories exist
os.makedirs('data/players', exist_ok=True)
os.makedirs('data/stats', exist_ok=True)
os.makedirs('logs/api', exist_ok=True)
os.makedirs('logs/collection', exist_ok=True)
os.makedirs('logs/errors', exist_ok=True) 