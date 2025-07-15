from app import create_app
from flask.cli import with_appcontext
import click
from flask_migrate import upgrade
import os

# Import database setup utilities and logger
from db.create_db import create_database, create_tables
from app.logger import setup_logger  # Adjust import based on your project structure

# Initialize logger
logger = setup_logger(__name__)

# Step 1: Ensure the database and tables are created before app starts
try:
    logger.info("Checking and creating database if necessary...")
    create_database()
    create_tables()
    logger.info("Database and tables are ready.")
except Exception as e:
    logger.error(f"Error during database setup: {e}")
    raise

# Step 2: Create the Flask application instance using factory pattern
app = create_app()
logger.info("Flask application instance created successfully.")

# Step 3: Define custom CLI command to apply migrations
@click.command("db-upgrade")
@with_appcontext
def db_upgrade_command():
    """
    Apply all pending database migrations.
    Equivalent to running: flask db upgrade
    """
    try:
        upgrade()
        logger.info("Database schema upgraded successfully.")
        click.echo("Database upgraded successfully.")
    except Exception as e:
        logger.error(f"Error applying database migrations: {e}")
        click.echo("Failed to upgrade database.")

# Step 4: Register custom command with Flask CLI
app.cli.add_command(db_upgrade_command)
logger.debug("Custom CLI command 'db-upgrade' registered with Flask.")

# Step 5: Run the app if executed directly
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Flask app on http://0.0.0.0:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
