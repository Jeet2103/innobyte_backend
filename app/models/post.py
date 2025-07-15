from app.extensions import db
from app.logger import setup_logger

# Initialize logger for the Post model
logger = setup_logger(__name__)

class Post(db.Model):
    """Model representing a blog post authored by a user."""
    
    __tablename__ = 'posts'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Post fields
    title = db.Column(db.String(150), nullable=False)  # Post title
    content = db.Column(db.Text, nullable=False)        # Post content body

    # Foreign Key to User (author)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Created timestamp
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())        # Auto-updated on edit

    # One-to-Many: A post can have multiple comments
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f"<Post {self.title}>"

# Log model load event
logger.info("Post model loaded and mapped to table 'posts'")
