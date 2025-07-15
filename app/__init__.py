from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt, ma
from app.routes.auth_routes import auth_bp
from app.routes.post_routes import post_bp
from app.routes.comment_routes import comment_bp
from app.logger import setup_logger
from flasgger import Swagger
from app.swagger_config import SWAGGER_TEMPLATE

# Initialize module-level logger
logger = setup_logger(__name__)

def create_app():
    """
    Application factory function.
    Creates and configures the Flask application instance using the factory pattern.
    """
    try:
        # Create Flask app instance
        app = Flask(__name__)
        logger.info("Flask app instance created.")
        
        # Load configuration from the Config class
        app.config.from_object(Config)
        logger.info("Configuration loaded into Flask app.")

        # Initialize Flask extensions
        db.init_app(app)
        logger.info("SQLAlchemy initialized.")

        migrate.init_app(app, db)
        logger.info("Flask-Migrate initialized.")

        jwt.init_app(app)
        logger.info("JWT Manager initialized.")

        ma.init_app(app)
        logger.info("Marshmallow initialized.")

        # Initialize Swagger UI with the provided template
        try:
            Swagger(app, template=SWAGGER_TEMPLATE)
            logger.info("Swagger UI initialized successfully.")
        except Exception as swagger_error:
            logger.warning(f"Swagger UI initialization failed: {swagger_error}")

        # Import models to register them with SQLAlchemy
        from app import models  # Required for Alembic and relationships
        logger.debug("Models imported and SQLAlchemy metadata registered.")

        # Register application blueprints with appropriate prefixes
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(post_bp, url_prefix='/api')
        app.register_blueprint(comment_bp, url_prefix='/api')
        logger.info("Blueprints registered successfully.")

        logger.info("Flask application setup completed successfully.")
        return app

    except Exception as e:
        logger.error(f"Application setup failed: {e}")
        raise
