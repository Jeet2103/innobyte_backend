from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models.post import Post
from app.logger import setup_logger

# Initialize logger for the schema module
logger = setup_logger(__name__)
logger.info("Initializing PostSchema for serialization and deserialization.")

class PostSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow schema for serializing and deserializing Post model instances.

    Features:
    - Auto-generates fields from the Post SQLAlchemy model
    - Validates required fields on load
    - Maintains field order for consistent API responses
    - Includes foreign keys (author_id)
    """
    class Meta:
        model = Post                # The associated SQLAlchemy model
        load_instance = True       # Deserialize into model instances
        include_fk = True          # Include foreign key fields
        ordered = True             # Maintain field order in output

    # Explicitly define fields for validation and documentation
    id = fields.Int(dump_only=True)             # Read-only unique identifier
    title = fields.Str(required=True)           # Post title (required)
    content = fields.Str(required=True)         # Post body content (required)
    author_id = fields.Int(required=True)       # Foreign key to User model
    created_at = fields.DateTime(dump_only=True)  # Timestamp of creation (read-only)

# Attempt to create schema instances with logging
try:
    post_schema = PostSchema()                 # For single post
    posts_schema = PostSchema(many=True)       # For list of posts
    logger.info("PostSchema instances initialized successfully.")

except Exception as e:
    logger.error(f"Failed to initialize PostSchema: {e}")
    raise
