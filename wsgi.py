"""WSGI entry point for production deployment (e.g., Gunicorn or uWSGI)."""

from app import create_app
from app.logger import setup_logger

# Initialize the logger
logger = setup_logger(__name__)
logger.info("Starting WSGI application setup...")

# Create the Flask app instance using the application factory
app = create_app()
logger.info("Flask application instance created successfully for WSGI deployment.")

# Optional: expose `app` as a module-level variable (default behavior for WSGI servers)
# WSGI servers like Gunicorn or uWSGI look for a variable named `app` by default.
