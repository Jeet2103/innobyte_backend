import pytest
from app import create_app
from app.extensions import db
from app.logger import setup_logger

# Initialize module-level logger
logger = setup_logger(__name__)

@pytest.fixture(scope='module')
def test_client():
    """
    Pytest fixture to set up a test client with an in-memory SQLite database.
    This runs once per test module and provides a clean test environment.
    """
    logger.info("Setting up test client with in-memory SQLite database.")
    
    try:
        # Create the Flask app instance using the factory pattern
        app = create_app()

        # Configure the app for testing
        app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use in-memory DB for fast tests
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JWT_SECRET_KEY": "test-secret"
        })
        logger.debug("Test configuration applied.")

        # Set up the test client and application context
        with app.test_client() as client:
            with app.app_context():
                db.create_all()
                logger.info("Database tables created successfully.")
                yield client  # Provide the test client to the test functions
                db.drop_all()
                logger.info("Database tables dropped after tests.")

    except Exception as e:
        logger.error(f"Error during test client setup or teardown: {e}")
        raise  # Re-raise to fail the test immediately
