"""Logging configuration for IRCTC booking bot"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    log_level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_dir: str = "logs"
) -> logging.Logger:
    """Setup logger with file and console handlers
    
    Args:
        name: Logger name
        log_level: Logging level (default: INFO)
        log_file: Log file name (default: {name}.log)
        log_dir: Log directory (default: logs)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Log file path
    if log_file is None:
        log_file = f"{name}.log"
    
    log_file_path = log_path / log_file
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get logger by name
    
    Args:
        name: Logger name
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
