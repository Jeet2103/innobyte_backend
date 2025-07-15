from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models.comment import Comment
from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)
logger.info("Initializing CommentSchema for Marshmallow serialization.")

class CommentSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow schema for serializing and deserializing Comment model instances.
    
    This schema supports:
    - Automatic field generation from SQLAlchemy model
    - Foreign key inclusion for relationships
    - Enforced field order for predictable output
    - Validation on required fields during load
    """
    class Meta:
        model = Comment                # Associated SQLAlchemy model
        load_instance = True          # Deserialize to model instances
        include_fk = True             # Include foreign keys in serialization
        ordered = True                # Ensure field order in output

    # Define fields explicitly for validation and clarity
    id = fields.Int(dump_only=True)            # Read-only field
    content = fields.Str(required=True)        # Required text content
    post_id = fields.Int(required=True)        # FK to associated post
    author_id = fields.Int(required=True)      # FK to comment's author
    created_at = fields.DateTime(dump_only=True)  # Timestamp, read-only

try:
    # Single comment schema instance
    comment_schema = CommentSchema()

    # Multiple comment instances
    comments_schema = CommentSchema(many=True)

    logger.info("CommentSchema instances created successfully.")

except Exception as e:
    logger.error(f"Failed to initialize CommentSchema: {e}")
    raise
