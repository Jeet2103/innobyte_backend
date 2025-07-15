from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models.user import User
from app.logger import setup_logger

# Initialize logger for the schema
logger = setup_logger(__name__)
logger.info("Initializing UserSchema for serialization and validation.")

class UserSchema(SQLAlchemyAutoSchema):
    """
    Marshmallow schema for serializing and deserializing User model instances.

    Notes:
    - Automatically maps fields from the User model
    - Password is excluded from output (only accepted on input)
    - Fields are ordered for consistent API responses
    """
    class Meta:
        model = User                  # Associated SQLAlchemy model
        load_instance = True         # Deserialize to model instances
        ordered = True               # Maintain field order in output

    # Define individual fields with validation and serialization rules
    id = fields.Int(dump_only=True)             # Unique identifier (read-only)
    username = fields.Str(required=True)        # Username (required)
    email = fields.Email(required=True)         # Email (validated as proper format)
    password = fields.Str(load_only=True)       # Password is only accepted, never returned
    created_at = fields.DateTime(dump_only=True)  # Account creation timestamp (read-only)

# Attempt to instantiate schema instances
try:
    user_schema = UserSchema()                  # For single user
    users_schema = UserSchema(many=True)        # For list of users
    logger.info("UserSchema instances created successfully.")

except Exception as e:
    logger.error(f"Failed to initialize UserSchema: {e}")
    raise
