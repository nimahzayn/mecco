"""
Logging Configuration Module

Provides centralized logging configuration for the application.
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: str = 'INFO',
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name: Logger name (usually __name__ of the module)
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string
    
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    # Create formatter
    if log_format is None:
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


def log_request(logger: logging.Logger, method: str, endpoint: str, status_code: int):
    """
    Log HTTP request details.
    
    Args:
        logger: Logger instance
        method: HTTP method (GET, POST, etc.)
        endpoint: API endpoint
        status_code: HTTP status code
    """
    logger.info(f"{method} {endpoint} - Status: {status_code}")


def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Log error with context.
    
    Args:
        logger: Logger instance
        error: Exception object
        context: Additional context information
    """
    logger.error(f"{context} - Error: {str(error)}", exc_info=True)