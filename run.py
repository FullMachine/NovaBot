"""
Script to run the Nova Sports Data API.
"""
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=True if os.getenv("ENVIRONMENT") == "development" else False,
        workers=int(os.getenv("API_WORKERS", 1)),
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
        timeout_keep_alive=int(os.getenv("API_TIMEOUT", 30))
    ) 