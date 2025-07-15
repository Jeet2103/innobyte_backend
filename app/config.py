import os
from dotenv import load_dotenv
from app.logger import setup_logger  # Adjust the import based on your structure

# Set up logger
logger = setup_logger(__name__)
logger.info("Loading environment variables from .env file.")

# Load environment variables from .env
load_dotenv()

class Config:
    """
    Central configuration class for the Flask application.
    Loads settings from environment variables (typically from a .env file).
    """

    # Load required configuration variables
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Log errors if critical environment variables are missing
    if not SQLALCHEMY_DATABASE_URI:
        logger.error("Missing required environment variable: DATABASE_URL")
        raise ValueError("DATABASE_URL must be set in the .env file.")
    else:
        logger.info("SQLALCHEMY_DATABASE_URI loaded successfully.")

    if not JWT_SECRET_KEY:
        logger.error("Missing required environment variable: JWT_SECRET_KEY")
        raise ValueError("JWT_SECRET_KEY must be set in the .env file.")
    else:
        logger.info("JWT_SECRET_KEY loaded successfully.")

    # Optional but recommended configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables event system for performance
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"  # Enable debug mode based on env

    logger.info(f"DEBUG mode set to: {DEBUG}")
    logger.info("Configuration loaded successfully.")
