import logging
import os

# Ensure the data folder exists for the log file
os.makedirs("data", exist_ok=True)

# Configure the logger
logging.basicConfig(
    filename="data/log.txt",  # Log file location
    level=logging.INFO,       # Default log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_info(message: str):
    """
    Logs an informational message.
    Args:
        message (str): The message to log.
    """
    logging.info(message)

def log_error(message: str):
    """
    Logs an error message.
    Args:
        message (str): The error message to log.
    """
    logging.error(message)

def log_debug(message: str):
    """
    Logs a debug message.
    Args:
        message (str): The debug message to log.
    """
    logging.debug(message)
