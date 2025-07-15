from app.logger import setup_logger

# Set up logger
logger = setup_logger(__name__)

# Swagger UI configuration template
try:
    SWAGGER_TEMPLATE = {
        "swagger": "2.0",
        "info": {
            "title": "RESTful Blog API",
            "description": "Documentation for the Blog API (Users, Posts, Comments)",
            "version": "1.0.0",
            "contact": {
                "name": "Jeet Nandigrami",
                "email": "jeetnandigrami2003@gmail.com"
            }
        },
        "basePath": "/api",  # Common API prefix (optional)
        "schemes": [
            "http", "https"
        ],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ],
        "tags": [
            {"name": "Auth", "description": "Register and Login"},
            {"name": "Posts", "description": "Create, view, update, and delete blog posts"},
            {"name": "Comments", "description": "Manage comments on posts"}
        ]
    }

    logger.info("Swagger template loaded successfully.")

except Exception as e:
    logger.error(f"Failed to load Swagger template: {str(e)}")
    SWAGGER_TEMPLATE = {}
