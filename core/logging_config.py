# -*- coding: utf-8 -*-
"""
Logging configuration for FTNatlink
Provides centralized logging setup for the entire application
"""

import logging
import sys
from pathlib import Path
import os

# Global flag to prevent multiple logging setups
_logging_configured = False


def setup_logging(log_level=logging.INFO):
    """
    Setup logging configuration for FTNatlink

    Args:
        log_level: Logging level (default: logging.INFO)
    """
    global _logging_configured

    # Prevent multiple setups
    if _logging_configured:
        return

    # Create logs directory if it doesn't exist
    try:
        # Handle PyInstaller path resolution
        if hasattr(sys, "_MEIPASS"):
            # Running as executable - log to user directory
            log_dir = Path.home() / "AppData" / "Local" / "FTNatlink" / "logs"
        else:
            # Running as script - log to project directory
            log_dir = Path(__file__).parent / "logs"

        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        # Fallback to current directory
        log_dir = Path.cwd()

    log_file = log_dir / "ftnatlink.log"

    # Configure logging format
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Remove existing handlers to prevent duplicates
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Configure root logger first
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # File handler
    try:
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # Log startup info
        logger = logging.getLogger(__name__)
        logger.info(f"Logging configured - Log file: {log_file}")

    except Exception as e:
        # If file logging fails, just use console
        logger = logging.getLogger(__name__)
        logger.warning(f"File logging failed ({e}), using console only")

    # Mark as configured
    _logging_configured = True


def get_logger(name):
    """
    Get a logger with the specified name

    Args:
        name: Logger name (usually __name__)

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


# Default logger for quick access
log = get_logger(__name__)
