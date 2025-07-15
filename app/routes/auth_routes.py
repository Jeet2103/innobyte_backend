from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.services.auth_service import register_user, authenticate_user
from app.logger import setup_logger
from flasgger import swag_from
import re

# Set up logger
logger = setup_logger(__name__)

# Define blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# Utility: Validate email using regex
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Utility: Validate password strength
def validate_password(password):
    """
    Password must have at least:
    - 8 characters
    - One uppercase letter
    - One lowercase letter
    - One number
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Register a new user',
    'description': 'Creates a new user with a validated username, email, and password.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'email': {'type': 'string'},
                'password': {'type': 'string'}
            },
            'required': ['username', 'email', 'password']
        }
    }],
    'responses': {
        201: {'description': 'User registered successfully'},
        400: {'description': 'Invalid input'},
        409: {'description': 'User already exists'}
    }
})
def register():
    """
    Registers a new user with validation.
    """
    if not request.is_json:
        logger.warning("Register request failed: Missing or invalid JSON.")
        return jsonify({"error": "Missing or invalid JSON"}), 400

    try:
        data = request.get_json()
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            logger.warning("Register request failed: Missing required fields.")
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400

        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']

        # Field validation
        if len(username) < 4:
            return jsonify({"error": "Username must be at least 4 characters"}), 400
        if not validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400
        if not validate_password(password):
            return jsonify({
                "error": "Password must be 8+ characters with at least one uppercase, one lowercase, and one number"
            }), 400

        # Attempt registration
        user, error = register_user(username, email, password)
        if error:
            logger.warning(f"Registration conflict: {error}")
            return jsonify({"error": error}), 409

        logger.info(f"User registered: {username} (ID: {user.id})")
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 201

    except Exception as e:
        logger.error(f"Unexpected error during registration: {e}")
        return jsonify({"error": "Registration failed", "details": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'summary': 'Log in a user',
    'description': 'Authenticates a user and returns a JWT access token.',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string'},
                'password': {'type': 'string'}
            },
            'required': ['username', 'password']
        }
    }],
    'responses': {
        200: {'description': 'Login successful, JWT token returned'},
        400: {'description': 'Missing credentials'},
        401: {'description': 'Invalid credentials'}
    }
})
def login():
    """
    Authenticates a user and returns a JWT token.
    """
    if not request.is_json:
        logger.warning("Login request failed: Missing JSON in request.")
        return jsonify({"error": "Missing JSON in request"}), 400

    try:
        data = request.get_json()
        required_fields = ['username', 'password']
        if not all(field in data for field in required_fields):
            logger.warning("Login request failed: Missing required fields.")
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400

        username = data['username'].strip()
        password = data['password']

        # Authenticate user
        user, error = authenticate_user(username, password)
        if error:
            logger.warning(f"Authentication failed for user: {username}")
            return jsonify({"error": error}), 401

        # Generate JWT token
        access_token = create_access_token(identity=user.id)

        logger.info(f"User logged in: {username} (ID: {user.id})")
        return jsonify({
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username
            }
        }), 200

    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        return jsonify({"error": "Login failed", "details": str(e)}), 500
