import logging
import os
from logging.handlers import RotatingFileHandler
from io import StringIO
from tkinter import Text


# Define a centralized log file path
LOG_FILE_PATH = "logs/actions.log"

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

# Configure the logger
logger = logging.getLogger("LibraryManagement")
logger.setLevel(logging.INFO)

# Rotating file handler to manage log file size
file_handler = RotatingFileHandler(
    LOG_FILE_PATH,
    maxBytes=5 * 1024 * 1024,  # 5 MB per log file
    backupCount=3  # Keep up to 3 backup log files
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)

# Stream handler for console and GUI output
console_stream = logging.StreamHandler()
console_formatter = logging.Formatter("%(message)s")
console_stream.setFormatter(console_formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_stream)

# Centralized log message buffer for GUI
log_buffer = StringIO()
buffer_handler = logging.StreamHandler(log_buffer)
buffer_formatter = logging.Formatter("%(message)s")
buffer_handler.setFormatter(buffer_formatter)
logger.addHandler(buffer_handler)

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

def get_gui_log():
    """
    Retrieves the log messages for GUI display.
    Returns:
        str: The accumulated log messages.
    """
    return log_buffer.getvalue()


class TkinterLogHandler(logging.Handler):
    """
    Custom log handler to send log messages to a Tkinter Text widget.
    """
    def __init__(self, text_widget: Text):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        log_entry = self.format(record)
        self.text_widget.insert("end", log_entry + "\n")
        self.text_widget.see("end")  # Automatically scroll to the end

