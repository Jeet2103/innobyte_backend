from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models.user import User
from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

def jwt_required_with_user(fn):
    """
    Custom decorator that enforces JWT authentication and injects the authenticated
    user object into the route handler.

    Usage:
        @jwt_required_with_user
        def your_route(current_user):
            ...

    Returns 401 if JWT is invalid or missing.
    Returns 404 if user from JWT is not found in the database.
    """

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        try:
            # Retrieve user ID from JWT payload
            user_id = get_jwt_identity()
            logger.debug(f"JWT identity extracted: user_id={user_id}")

            # Look up user in the database
            user = User.query.get(user_id)
            if not user:
                logger.warning(f"User not found for user_id={user_id}")
                return jsonify({"error": "User not found."}), 404

            logger.info(f"Authenticated user: {user.username} (ID: {user.id})")
            return fn(user, *args, **kwargs)

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return jsonify({
                "error": "Authentication failed",
                "details": str(e)
            }), 401

    return wrapper
