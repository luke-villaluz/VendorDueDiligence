"""
Logging configuration for Vendor Due Diligence Automation Tool.
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from src.config.settings import settings

def setup_logger(name: str = "vendor_dd", log_file: Optional[Path] = None) -> logging.Logger:
    """
    Set up a logger with both file and console output.
    
    Args:
        name: Logger name
        log_file: Optional log file path, defaults to settings.log_file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, settings.log_level))
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file is None:
        log_file = settings.log_file
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    return logger

# Global logger instance
logger = setup_logger()
