from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from app.logger import setup_logger  # Adjust the import path as necessary

# Set up module-level logger
logger = setup_logger(__name__)
logger.info("Starting Flask extension initialization.")

# Initialize Flask extensions with error handling
try:
    # SQLAlchemy: ORM for database interactions
    db = SQLAlchemy()
    logger.info("SQLAlchemy initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize SQLAlchemy: {e}")
    raise

try:
    # Flask-Migrate: Handles DB migrations using Alembic
    migrate = Migrate()
    logger.info("Flask-Migrate initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Flask-Migrate: {e}")
    raise

try:
    # JWTManager: Handles JWT-based authentication
    jwt = JWTManager()
    logger.info("JWTManager initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize JWTManager: {e}")
    raise

try:
    # Marshmallow: Used for serialization and validation
    ma = Marshmallow()
    logger.info("Marshmallow initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Marshmallow: {e}")
    raise

logger.info("All Flask extensions initialized without errors.")
