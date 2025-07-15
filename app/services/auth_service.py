from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db
from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def register_user(username, email, password):
    """
    Registers a new user if the username and email are unique.

    Parameters:
        username (str): Desired username
        email (str): User's email address
        password (str): Plain-text password

    Returns:
        tuple: (User object, None) on success
               (None, str error message) on failure
    """
    logger.info(f"Attempting to register user: {username} ({email})")

    try:
        # Check for existing username or email
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            logger.warning(f"Registration failed: Username or email already exists for {username}")
            return None, "Username or email already exists."

        # Hash the password and create new user
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        logger.info(f"User registered successfully: {username} (ID: {user.id})")

        return user, None

    except Exception as e:
        logger.error(f"Error during user registration for {username}: {e}")
        return None, "An error occurred during registration."


def authenticate_user(username, password):
    """
    Authenticates a user by verifying their credentials.

    Parameters:
        username (str): Username used to login
        password (str): Plain-text password

    Returns:
        tuple: (User object, None) on successful authentication
               (None, str error message) on failure
    """
    logger.info(f"Authenticating user: {username}")

    try:
        user = User.query.filter_by(username=username).first()

        # Verify password hash
        if user and check_password_hash(user.password, password):
            logger.info(f"User authenticated successfully: {username}")
            return user, None

        logger.warning(f"Authentication failed for user: {username}")
        return None, "Invalid credentials."

    except Exception as e:
        logger.error(f"Error during authentication for {username}: {e}")
        return None, "An error occurred during authentication."
