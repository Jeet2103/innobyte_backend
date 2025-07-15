# app/models/__init__.py

# Import all models to ensure SQLAlchemy registers them correctly
# This is required for Alembic autogeneration and for initializing relationships
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment

# Optional: Log successful model registration
from app.logger import setup_logger
logger = setup_logger(__name__)
logger.info("All model classes imported: User, Post, Comment")
