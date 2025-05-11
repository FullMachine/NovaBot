"""
Server configuration settings
"""
import os
from typing import Dict, Any

class ServerConfig:
    """Server configuration class"""
    
    def __init__(self):
        # API Server settings
        self.host = os.getenv("API_HOST", "0.0.0.0")
        self.port = int(os.getenv("API_PORT", "8001"))  # Using 8001 instead of 8000
        self.reload = os.getenv("API_RELOAD", "true").lower() == "true"
        self.workers = int(os.getenv("API_WORKERS", "1"))
        self.timeout = int(os.getenv("API_TIMEOUT", "30"))
        
        # Process management
        self.pid_file = "api_server.pid"
        
    def get_uvicorn_config(self) -> Dict[str, Any]:
        """Get Uvicorn server configuration"""
        return {
            "host": self.host,
            "port": self.port,
            "reload": self.reload,
            "workers": self.workers if not self.reload else None,
            "timeout_keep_alive": self.timeout
        }
        
    def save_pid(self) -> None:
        """Save the current process ID"""
        with open(self.pid_file, "w") as f:
            f.write(str(os.getpid()))
            
    def load_pid(self) -> int:
        """Load the saved process ID"""
        try:
            with open(self.pid_file, "r") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return None
            
    def cleanup_pid(self) -> None:
        """Remove the PID file"""
        try:
            os.remove(self.pid_file)
        except FileNotFoundError:
            pass 