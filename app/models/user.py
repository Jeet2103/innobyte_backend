from app.extensions import db
from app.logger import setup_logger

# Initialize logger for User model
logger = setup_logger(__name__)

class User(db.Model):
    """Model representing a registered user."""

    __tablename__ = 'users'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # User credentials and identifiers
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(120), unique=True, nullable=False)    # Unique email address
    password = db.Column(db.String(200), nullable=False)              # Hashed password

    # Reverse relationships
    posts = db.relationship('Post', backref='author', lazy=True)      # One-to-many: User → Posts
    comments = db.relationship('Comment', backref='author', lazy=True)  # One-to-many: User → Comments

    def __repr__(self):
        return f"<User {self.username}>"

# Log model registration
logger.info("User model loaded and mapped to table 'users'")
