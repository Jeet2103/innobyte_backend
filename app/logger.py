import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os

def setup_logger(name, log_file='app.log', level=logging.INFO):
    """Setup and configure a logger with timestamp and filename."""
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Create formatter that includes timestamp, filename, and line number
    formatter = logging.Formatter(
        '[%(asctime)s] - [%(name)s] - [%(filename)s] - %(lineno)d - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create rotating file handler (max 5 files, 5MB each)
    file_handler = RotatingFileHandler(
        filename=f'logs/{log_file}',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Get the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Example usage
if __name__ == '__main__':
    logger = setup_logger(__name__)
    
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    try:
        1 / 0
    except Exception as e:
        logger.exception("Exception occurred: %s", str(e))