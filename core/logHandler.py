"""
Centralized log handler for FTNatlink application
Provides a simple import: from logHandler import log
"""

try:
    from core.logging_config import get_logger

    log = get_logger("FTNatlink")
except ImportError:
    import logging

    log = logging.getLogger("FTNatlink")
    # Set up basic logging if core.logging_config is not available
    if not log.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)
        log.setLevel(logging.INFO)
