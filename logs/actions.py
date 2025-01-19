import logging
import os
from logging.handlers import RotatingFileHandler

# Define a centralized log file path
LOG_FILE_PATH = "logs/actions.log"

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# Configure the logger
logger = logging.getLogger("LibraryManagement")
logger.setLevel(logging.INFO)

# Rotating file handler to manage log file size
handler = RotatingFileHandler(
    LOG_FILE_PATH,
    maxBytes=5 * 1024 * 1024,  # 5 MB per log file
    backupCount=3  # Keep up to 3 backup log files
)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Logging functions
def log_info(message: str):
    """
    Logs an informational message.
    Args:
        message (str): The message to log.
    """
    logger.info(message)

def log_error(message: str):
    """
    Logs an error message.
    Args:
        message (str): The error message to log.
    """
    logger.error(message)

def log_debug(message: str):
    """
    Logs a debug message.
    Args:
        message (str): The debug message to log.
    """
    logger.debug(message)