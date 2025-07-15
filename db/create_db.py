import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
from app.logger import setup_logger  # Adjust this import based on your structure

# Initialize logger
logger = setup_logger(__name__)

# Load environment variables from .env file
load_dotenv()

# Load DB configuration from environment
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def create_database():
    """
    Connects to the default 'postgres' database and creates a new database (DB_NAME)
    if it doesn't already exist.
    """
    try:
        logger.info("Connecting to default 'postgres' database to check/create target database.")

        # Step 1: Connect to default database
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Step 2: Check if the target database already exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            logger.info(f"Database '{DB_NAME}' created successfully.")
        else:
            logger.info(f"ℹDatabase '{DB_NAME}' already exists.")

        cur.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error creating database '{DB_NAME}': {e}")
        raise


def create_tables():
    """
    Connects to the target database and creates required tables if they do not exist.
    """
    try:
        logger.info(f"Connecting to '{DB_NAME}' database to create tables.")

        # Step 3: Connect to the target database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Step 4: Create necessary tables
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) NOT NULL UNIQUE,
            email VARCHAR(120) NOT NULL UNIQUE,
            password VARCHAR(200) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(150) NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS comments (
            id SERIAL PRIMARY KEY,
            post_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """)

        conn.commit()
        logger.info("Tables created successfully in the database.")
        cur.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error creating tables in '{DB_NAME}': {e}")
        raise


if __name__ == "__main__":
    logger.info("Starting database initialization process.")
    create_database()
    create_tables()
    logger.info("Database setup completed successfully.")
