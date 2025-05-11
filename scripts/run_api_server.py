"""
Run the FastAPI server independently
"""
import os
import sys
import signal
import uvicorn
from app.config.server_config import ServerConfig

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\nShutting down API server...")
    config.cleanup_pid()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Load configuration
    config = ServerConfig()
    
    # Save PID for external management
    config.save_pid()
    
    try:
        # Run the server
        uvicorn.run(
            "app.main:app",
            **config.get_uvicorn_config()
        )
    finally:
        # Clean up on exit
        config.cleanup_pid() 