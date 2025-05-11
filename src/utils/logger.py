"""
Logging configuration for the NBA Data Analytics Platform.
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from .config import LOGS_DIR, LOG_LEVEL, LOG_FORMAT

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name: Name of the logger
        log_file: Optional log file name (will be created in LOGS_DIR)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log_file is specified
    if log_file:
        log_path = Path(LOGS_DIR) / log_file
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create default logger
default_logger = setup_logger('nova_proxy', 'nova_proxy.log') 